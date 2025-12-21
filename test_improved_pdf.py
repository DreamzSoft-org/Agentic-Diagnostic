from utils.pdf_generator import PDFReportGenerator

# Create an instance of the PDF generator
generator = PDFReportGenerator()

# Test with a comprehensive sample report content
sample_report = """
## CLINICAL NOTES
Patient presented with symptoms of fever and cough lasting 3 days.
Vital signs: Temperature 101.2°F, Blood pressure 120/80 mmHg, Heart rate 88 bpm.

## LABORATORY RESULTS
Complete Blood Count:
- White Blood Cells: 12.5 K/uL (High)
- Red Blood Cells: 4.5 M/uL (Normal)
- Hemoglobin: 13.2 g/dL (Normal)
- Platelets: 250 K/uL (Normal)

C-Reactive Protein: 15 mg/L (Elevated)

## DIAGNOSIS
- Upper Respiratory Tract Infection
- Mild dehydration

## TREATMENT PLAN
- Prescribe Amoxicillin 500mg TID for 7 days
- Advise increased fluid intake
- Follow up in 1 week if symptoms persist
- Recommend rest and over-the-counter fever reducer as needed

## RECOMMENDATIONS
- Monitor temperature twice daily
- Return if fever persists beyond 3 days of treatment
- Maintain adequate hydration
- Avoid strenuous activities until recovery

## ASSESSMENT
Patient is expected to recover fully with the prescribed treatment.
Symptoms should resolve within 5-7 days.
"""

# Test with patient info
patient_info = {
    "patient_name": "John Doe",
    "age": "45",
    "gender": "Male",
    "patient_id": "P-2025-001",
    "date_of_birth": "1978-05-15",
    "visit_date": "2025-12-18"
}

print("Generating improved test PDF report...")
pdf_bytes = generator.generate_pdf_report(sample_report, patient_info)

# Save the PDF to a file
with open('improved_test_report.pdf', 'wb') as f:
    f.write(pdf_bytes)

print("Improved test PDF generated successfully!")
print(f"PDF size: {len(pdf_bytes)} bytes")
print("Improved test PDF saved as improved_test_report.pdf")