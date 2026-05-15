# app.py
import streamlit as st
import os
from utils.file_handler import FileHandler, PatientManager
from agents.diagnostic_agent import DiagnosticAgent
from config.settings import settings
from utils.pdf_generator import PDFReportGenerator
import pandas as pd
from tempfile import NamedTemporaryFile
import sqlite3
from datetime import datetime
from utils.data_parser import MedicalDataParser

# Page configuration
st.set_page_config(
    page_title="Smart Clinic Diagnostic Agent",
    page_icon="🏥",
    layout="wide"
)

# Initialize session state
if 'clinical_case' not in st.session_state:
    st.session_state.clinical_case = ""
if 'clinical_notes' not in st.session_state:
    st.session_state.clinical_notes = ""
if 'lab_data' not in st.session_state:
    st.session_state.lab_data = ""
if 'image_findings' not in st.session_state:
    st.session_state.image_findings = ""
if 'documents' not in st.session_state:
    st.session_state.documents = ""
if 'document_types' not in st.session_state:
    st.session_state.document_types = {}
if 'uploaded_files_info' not in st.session_state:
    st.session_state.uploaded_files_info = []
if 'analysis_results' not in st.session_state:
    st.session_state.analysis_results = None
if 'patient_id' not in st.session_state:
    st.session_state.patient_id = ""
if 'patient_name' not in st.session_state:
    st.session_state.patient_name = ""
if 'patient_age' not in st.session_state:
    st.session_state.patient_age = 30
if 'patient_gender' not in st.session_state:
    st.session_state.patient_gender = "Male"
if 'show_results' not in st.session_state:
    st.session_state.show_results = False

def main():
    # Add custom CSS from external file
    try:
        with open("static/css/style.css", "r") as f:
            css = f.read()
            st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning("CSS file not found. Using default styling.")

    # Header
    col1, col2, col3 = st.columns([0.5, 3, 0.5])
    with col1:
        st.write(' ')
    
    with col2:
        st.image("smile-ihs.png", width="content")
        
    with col3:
        st.write(' ')
    #st.markdown('<div class="header"><h1>🏥 Advanced Clinical Diagnostic Agent</h1><p>AI-powered medical data analysis & diagnostic assistance</p></div>', unsafe_allow_html=True)

    # Initialize components
    file_handler = FileHandler()
    patient_manager = PatientManager()
    diagnostic_agent = DiagnosticAgent(api_key=settings.OPENAI_API_KEY)

    # Top section with Patient Info and Clinical Input
    col1, col2 = st.columns([1, 2])

    with col1:
        st.markdown('<div class="section-header"><span>👤</span>Patient Information</div>', unsafe_allow_html=True)
        
        patient_id = st.text_input("Patient ID", value=st.session_state.patient_id, key="patient_id_input")
        st.session_state.patient_id = patient_id

        patient_name = st.text_input("Patient Name", value=st.session_state.patient_name, key="patient_name_input")
        st.session_state.patient_name = patient_name

        patient_age = st.number_input("Age", min_value=0, max_value=150, value=st.session_state.patient_age, key="patient_age_input")
        st.session_state.patient_age = patient_age

        patient_gender = st.selectbox("Gender", ["Male", "Female", "Other"], index=["Male", "Female", "Other"].index(st.session_state.patient_gender), key="patient_gender_input")
        st.session_state.patient_gender = patient_gender
        
        if patient_id and patient_name:
            patient_manager.create_patient(patient_id, patient_name, patient_age, patient_gender)

    with col2:
        st.markdown('<div class="section-header"><span>📄</span>Clinical Input</div>', unsafe_allow_html=True)
        
        clinical_case = st.text_area(
            "Clinical Case Description",
            value=st.session_state.clinical_case,
            height=150,
            key="clinical_case_input",
            help="Enter clinical case details, patient symptoms, medical history, chief complaint, etc."
        )
        st.session_state.clinical_case = clinical_case

        clinical_notes = st.text_area(
            "Clinical Messages/Notes",
            value=st.session_state.clinical_notes,
            height=150,
            key="clinical_notes_input",
            help="Enter clinical messages, nursing notes, physician observations..."
        )
        st.session_state.clinical_notes = clinical_notes

    # Data Upload Sections
    st.markdown('<div class="section-header"><span>📁</span>Clinical Documents & Data</div>', unsafe_allow_html=True)
    
    doc_col, data_col = st.columns(2)

    with doc_col:
        st.markdown('**Upload Clinical Documents**', unsafe_allow_html=True)
        uploaded_docs = st.file_uploader(
            "Upload PDF, JPG, PNG, etc.",
            type=['pdf', 'jpg', 'jpeg', 'png', 'gif', 'bmp', 'tiff', 'webp'],
            accept_multiple_files=True,
            key="doc_upload"
        )
        if uploaded_docs:
            for doc in uploaded_docs:
                file_handler.save_uploaded_file(doc, folder="documents", patient_id=st.session_state.patient_id or "unknown")
            st.success(f"{len(uploaded_docs)} document(s) uploaded.")

        st.markdown('**Manual Text Entry**', unsafe_allow_html=True)
        manual_doc_text = st.text_area(
            "Paste clinical documents, lab reports, etc.",
            value=st.session_state.documents,
            height=200,
            key="manual_doc_input"
        )
        st.session_state.documents = manual_doc_text

    with data_col:
        st.markdown('**Upload Lab Results**', unsafe_allow_html=True)
        uploaded_excel = st.file_uploader(
            "Upload Excel, CSV",
            type=['xlsx', 'xls', 'csv'],
            key="excel_upload"
        )
        if uploaded_excel:
            file_handler.save_uploaded_file(uploaded_excel, folder="excel", patient_id=st.session_state.patient_id or "unknown")
            st.success(f"Successfully uploaded {uploaded_excel.name}")
        
        st.markdown('**Manual Data Entry**', unsafe_allow_html=True)
        manual_lab_data = st.text_area(
            "Enter lab values, vital signs, etc.",
            value=st.session_state.lab_data,
            height=200,
            key="manual_lab_input"
        )
        st.session_state.lab_data = manual_lab_data


    # Medical Image Analysis
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-header"><span>🖼️</span>Medical Image Analysis</div>', unsafe_allow_html=True)
    
    uploaded_images = st.file_uploader(
        "Upload Medical Images",
        type=['dcm', 'dicom', 'jpg', 'jpeg', 'png', 'gif', 'bmp', 'tiff', 'webp'],
        accept_multiple_files=True,
        key="image_upload"
    )
    
    if uploaded_images:
        for img in uploaded_images:
            file_handler.save_uploaded_file(img, folder="images", patient_id=st.session_state.patient_id or "unknown")
        st.success(f"{len(uploaded_images)} image(s) uploaded.")
        
        # Display images in columns
        img_cols = st.columns(len(uploaded_images))
        for i, img in enumerate(uploaded_images):
            with img_cols[i]:
                st.image(img, caption=f"Medical Image: {img.name}", use_column_width=True)

    image_description = st.text_area(
        "Manual Image Description Entry",
        value=st.session_state.image_findings,
        height=150,
        key="image_desc_input",
        help="Describe medical image findings, radiology reports, or imaging observations..."
    )
    st.session_state.image_findings = image_description
    st.markdown('</div>', unsafe_allow_html=True)

    # Action Buttons
    st.markdown('<div class="action-buttons">', unsafe_allow_html=True)
    btn_col1, btn_col2 = st.columns(2)
    with btn_col1:
        if st.button("🩺 Analyze Clinical Case", key="analyze_btn", type="primary"):
            with st.spinner("Analyzing clinical case..."):
                all_documents = st.session_state.documents
                if uploaded_docs:
                    for doc in uploaded_docs:
                        all_documents += f"\n\n--- {doc.name} ---\nContent of {doc.name}"

                all_lab_data = st.session_state.lab_data
                if uploaded_excel:
                    all_lab_data += f"\n\n--- {uploaded_excel.name} ---\nContent of {uploaded_excel.name}"

                all_image_findings = st.session_state.image_findings
                if uploaded_images:
                     for img in uploaded_images:
                        all_image_findings += f"\n\n--- {img.name} ---\nAnalysis of {img.name}"

                results = diagnostic_agent.analyze_case(
                    clinical_case=st.session_state.clinical_case,
                    clinical_notes=st.session_state.clinical_notes,
                    lab_data=all_lab_data,
                    image_findings=all_image_findings,
                    documents=all_documents,
                    document_types="" # Simplified
                )
                st.session_state.analysis_results = results
                st.session_state.show_results = True

    with btn_col2:
        if st.button("🗑️ Clear All", key="clear_btn"):
            for key in st.session_state.keys():
                if key not in ['analysis_results', 'show_results']:
                    st.session_state[key] = "" if isinstance(st.session_state[key], str) else []
            st.session_state.patient_age = 30
            st.session_state.patient_gender = "Male"
            st.session_state.analysis_results = None
            st.session_state.show_results = False
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

    # Diagnostic Results
    if st.session_state.show_results and st.session_state.analysis_results:
        results = st.session_state.analysis_results
        st.markdown('<div class="diagnostic-results-section">', unsafe_allow_html=True)
        st.markdown('<div class="section-header"><span>📈</span>Diagnostic Results</div>', unsafe_allow_html=True)

        if results.get("error"):
            st.error(results["error"])
        else:
            # Prepare patient info for the PDF
            patient_info = {
                "patient_id": st.session_state.patient_id or "Unknown",
                "patient_name": st.session_state.patient_name or "Unknown",
                "patient_age": st.session_state.patient_age,
                "patient_gender": st.session_state.patient_gender
            }

            # Generate report content
            report_content = results.get("formatted_report", "No report available.")

            st.markdown('**Summary**')
            st.info(results.get("summary", "No summary available."))

            st.markdown('**Detailed Diagnostic Analysis**')
            st.markdown(results.get("diagnostic_analysis", "No analysis available."))

            st.markdown('**Formatted Medical Report**')
            st.markdown(results.get("formatted_report", "No report available."))

            # --- DEBUGGING BLOCK ---
            st.error("DEBUG: Please run the analysis, then copy ALL the text from the two boxes below and paste it in the chat.")
            st.subheader("Patient Info:")
            st.text(str(patient_info))
            st.subheader("Raw Report Content:")
            st.text(str(report_content))
            # --- END DEBUGGING BLOCK ---

            # Generate PDF and make it available for download
            pdf_generator = PDFReportGenerator()
            pdf_bytes = bytes(pdf_generator.generate_pdf_report(report_content, patient_info))

            # Add PDF download button
            st.markdown('**Download Report**')
            st.download_button(
                label="📥 Download Diagnostic Report as PDF",
                data=pdf_bytes,
                file_name=f"diagnostic_report_{st.session_state.patient_id or 'unknown'}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                mime="application/pdf",
                key="pdf_download_final"
            )

            # Cloud Healthcare API Section
            #st.markdown("---")
            #st.markdown("**Cloud Healthcare Integration**")
            
            #if not gcp_handler.available:
            #    st.info("💡 Cloud Healthcare API is not configured. Add your GCP credentials to the `.env` file to enable cloud storage.")
            #else:
            #    if st.button("☁️ Upload Report to Google Cloud Healthcare API", key="gcp_upload_btn"):
            #        with st.spinner("Uploading to Google Cloud..."):
            #            res = gcp_handler.store_diagnostic_report(
            #                patient_id=st.session_state.patient_id or "unknown",
            #                report_text=report_content,
            #                diagnosis=results.get("summary", "No summary")
            #            )
            #            if "success" in res:
            #                st.success(f"Successfully uploaded to FHIR Store! Resource: {res['name']}")
            #            else:
            #                st.error(f"Upload failed: {res.get('error')}")

    # Close the diagnostic results section div
    st.markdown('</div>', unsafe_allow_html=True)

    # Footer
    st.markdown('<div class="footer"><p>🏥 Smart Clinical Agent v1.0 | AI-Powered Diagnostics</p></div>', unsafe_allow_html=True)


if __name__ == "__main__":
    main()
