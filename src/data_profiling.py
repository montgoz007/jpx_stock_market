import os
import sys
import pandas as pd
from ydata_profiling import ProfileReport

def generate_profile(subfolder_path):
    # Define the output folder outside of the src folder
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    output_folder = os.path.join(project_root, "data_profiles")
    
    # Check if the output folder exists, if not, create it
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Loop through all CSV files in the subfolder
    for root, _, files in os.walk(subfolder_path):
        #print(subfolder_path)
        for file in files:
            if file.endswith(".csv"):
                csv_path = os.path.join(root, file)
                
                # Load CSV data
                try:
                    df = pd.read_csv(csv_path)
                except Exception as e:
                    print(f"Error reading {csv_path}: {e}")
                    continue
                
                # Generate profile report
                profile = ProfileReport(df, title=f"Profile of {file}", explorative=True)
                
                # Define the output path for the HTML profile
                output_file = os.path.join(output_folder, f"{file.replace('.csv', '')}_profile.html")
                
                # Save profile report to HTML
                profile.to_file(output_file)
                print(f"Profile saved for {file} at {output_file}")

if __name__ == "__main__":
    # Ensure correct number of arguments
    if len(sys.argv) != 2:
        print("Usage: python generate_profiles.py <subfolder_path>")
        sys.exit(1)

    # Get the subfolder argument
    subfolder_path = sys.argv[1]

    # Run the profile generation
    generate_profile(subfolder_path)
