import os
import sys
import pandas as pd

def is_numeric_like(series):
    # Check if all non-null values can be converted to numeric
    return series.dropna().apply(lambda x: isinstance(x, str) and x.replace('.', '', 1).isdigit()).all()

def process_csv(file_path):
    # Read the CSV file into a DataFrame
    try:
        # First, try loading the CSV without specifying 'Date'
        df = pd.read_csv(file_path)
        
        # If 'Date' column exists, parse it as a date
        if 'Date' in df.columns:
            df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return None

    # Loop through each column
    for col in df.columns:
        # Skip datetime columns
        if not pd.api.types.is_datetime64_any_dtype(df[col]):
            # Check if the column contains numeric-like values
            if is_numeric_like(df[col]):
                df[col] = pd.to_numeric(df[col], errors='coerce')
    
    return df

def main(input_folder):
    # Create a processed folder if it doesn't exist
    output_folder = os.path.join("data", "processed")
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Process all CSV files in the input folder and its subfolders
    for root, _, files in os.walk(input_folder):
        for file in files:
            if file.endswith(".csv"):
                csv_path = os.path.join(root, file)

                # Process the CSV file
                processed_df = process_csv(csv_path)
                
                if processed_df is not None:
                    # Construct the corresponding output path
                    relative_path = os.path.relpath(root, input_folder)
                    output_subfolder = os.path.join(output_folder, relative_path)
                    
                    # Create subfolders in the processed directory as needed
                    if not os.path.exists(output_subfolder):
                        os.makedirs(output_subfolder)
                    
                    # Save the processed DataFrame to a new CSV file in the corresponding processed subfolder
                    output_file_path = os.path.join(output_subfolder, file)
                    processed_df.to_csv(output_file_path, index=False)
                    print(f"Processed and saved: {output_file_path}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python process_data.py <input_folder>")
        sys.exit(1)

    input_folder = sys.argv[1]
    main(input_folder)
