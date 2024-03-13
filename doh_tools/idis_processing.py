#%%
import pandas as pd
import os
import zipfile

def process_idis_fwf(filename):
    '''
    Process the IDIS FWF Export from HUD.

    This function takes a fixed-width IDIS file, and coverts it to a pandas df. 

    Parameters:
        - filename: Path to the fixed-width IDIS file

    Returns:
        - Pandas df
    '''
    # Define an empty list to store column specifications
    col_specs = []

    # Read the fixed-width file
    with open(filename, 'r') as file:
        # Skip the first 5 lines
        for _ in range(5):
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



def idis_fwf_to_csv(input_path, output_folder_path):
    '''
    Process the IDIS FWF Export from HUD.

    This function takes a path to a folder with FWF IDIS files or zipped folders with said files, and writes them out as CSVs to a defined output folder. 

    Parameters:
        - input_path: Path to the fixed-width IDIS files and/or zipped folders
        - output_folder_path: Path to the folder you want the csvs written out to

    Returns:
        - All content that was fwfs as csvs
    '''
    if not os.path.exists(input_path):
        print("The path does not exist.")
        return

    for item in os.listdir(input_path):
        item_path = os.path.join(input_path, item)
        if os.path.isfile(item_path):
            if item.lower().endswith('.txt'):
                df = process_idis_fwf(item_path)
                out_item = os.path.splitext(item)[0] + '.csv'
                out_path = os.path.join(output_folder_path, out_item)
                df.to_csv(out_path, index=False)
            elif zipfile.is_zipfile(item_path):
                extract_zip(item_path)
                extract_path = os.path.join(input_path, os.path.splitext(item)[0])
                idis_fwf_to_csv(extract_path, output_folder_path)
            else:
                print(f"{item} is not a text file or zipped folder, skipping.")
        elif os.path.isdir(item_path):
            idis_fwf_to_csv(item_path, output_folder_path)

