from utils.icd10_processor import ICD10Processor
import os

def main():
    print("Starting ICD-10 Agent Training...")
    print("This will parse 'ICD-10-CM.txt' and index it for the Diagnostic Agent.")
    
    file_path = "TrainData\ICD-10-CM.txt" + "TrainData\Corpus100_DM_pts_2844_9304_33185_expanded.xlsx"
    if not os.path.exists(file_path):
        print(f"Error: {file_path} not found in the current directory.")
        return

    processor = ICD10Processor()
    success, message = processor.parse_and_load(file_path)
    
    if success:
        print("✅ Training Complete!")
        print(message)
        print("\nThe Diagnostic Agent is now 'trained' on ICD-10 data and will include official codes in its reports.")
    else:
        print("❌ Training Failed.")
        print(message)

if __name__ == "__main__":
    main()
