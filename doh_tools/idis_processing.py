import pandas as pd
import os
import zipfile
import re

def process_idis_fwf(filename):
    '''
    Process the IDIS FWF Export from HUD.

    This function takes a fixed-width IDIS file, and converts it to a pandas DataFrame.

    Parameters:
        - filename: Path to the fixed-width IDIS file

    Returns:
        - Pandas DataFrame
    '''
    # Define an empty list to store column specifications
    col_specs = []

    # Read the fixed-width file
    with open(filename, 'r') as file:
        # Skip line 1
        next(file)
        
        # Read in line 2
        table_name1 = file.readline().strip()

        # Skip Line 3
        next(file)

        # Read in line 4 as table name
        table_name2 = file.readline().strip()

        # Skip line 5
        next(file)

        # Read the file line by line
        for line in file:
            line = line.strip()
            if line:  # If the line is not empty
                # Extract column position, name, and type
                col_spec_parts = line.split()
                start = int(col_spec_parts[0].split('-')[0])
                end = int(col_spec_parts[0].split('-')[1])
                name = col_spec_parts[1]

                # Check for duplicate column names
                suffix = 1
                orig_name = name
                while name in [col[2] for col in col_specs]:
                    name = f"{orig_name}_{suffix}"
                    suffix += 1

                col_specs.append((start, end, name))
            else:
                # Break if a blank line is encountered
                break

        # Read the data into a DataFrame using the extracted column specifications
        df = pd.read_fwf(file, colspecs=[(spec[0]-1, spec[1]) for spec in col_specs], names=[spec[2] for spec in col_specs])

        # Add the TABLE_NAME column to the DataFrame
        table_name = table_name1 + ' ' + table_name2
        table_name = table_name.replace('*', '')
        table_name = re.sub(r'\s+', ' ', table_name).strip()
        table_name = table_name.replace(' ', '_').lower()
        df['TABLE_NAME'] = table_name

    return df



def extract_zip(zip_path):
    '''
    Extracts zipped folder contents to regular folder, deletes zipped folder after.

    Parameters:
        - zip_path: Path to the zipped folder

    Returns:
        - Extracted contents in regular folder
    '''
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        folder_name = os.path.splitext(os.path.basename(zip_path))[0]
        extract_dir = os.path.join(os.path.dirname(zip_path), folder_name)
        zip_ref.extractall(extract_dir)

    # Remove the zip file after extraction
    os.remove(zip_path)



def idis_fwf_to_file(input_path, output_folder_path, output_format='csv'):
    '''
    Process the IDIS FWF Export from HUD.

    This function takes a path to a folder with FWF IDIS files or zipped folders with said files, and writes them out as CSVs or Parquet files to a defined output folder.

    Parameters:
        - input_path: Path to the fixed-width IDIS files and/or zipped folders
        - output_folder_path: Path to the folder you want the files written out to
        - output_format: Output format, either 'csv' or 'parquet'. Default is 'csv'.

    Returns:
        - All content that was fwfs as csvs or parquet files
    '''
    if not os.path.exists(input_path):
        print("The path does not exist.")
        return

    for item in os.listdir(input_path):
        item_path = os.path.join(input_path, item)
        if os.path.isfile(item_path):
            if item.lower().endswith('.txt'):
                df = process_idis_fwf(item_path)
                out_item = df['TABLE_NAME'][0]
                if output_format == 'csv':
                    out_path = os.path.join(output_folder_path, out_item + '.csv')
                    df.to_csv(out_path, index=False)
                elif output_format == 'parquet':
                    out_path = os.path.join(output_folder_path, out_item + '.parquet')
                    df.to_parquet(out_path, index=False)
                else:
                    print("Unsupported output format. Please choose either 'csv' or 'parquet'.")
            elif zipfile.is_zipfile(item_path):
                extract_zip(item_path)
                extract_path = os.path.join(input_path, os.path.splitext(item)[0])
                idis_fwf_to_file(extract_path, output_folder_path, output_format)
            else:
                print(f"{item} is not a text file or zipped folder, skipping.")
        elif os.path.isdir(item_path):
            idis_fwf_to_file(item_path, output_folder_path, output_format)