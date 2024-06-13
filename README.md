# rwend-tools
A collection of helper functions designed to consolidate some useful utilities I often use, and to gain experience with publishing packages. This package includes various functions for common tasks such as data manipulation, file handling, logging and more.
## Installation Instructions
```bash
pip install rwend_tools
```
## Package Structure
```bash
.
├── rwend_tools
│   ├── custom_logging.py
│   ├── google_helpers.py
│   ├── pums.py
│   └── utils.py
```

## Usage Guide
### 1. PUMS
  - This module downloads PUMS (Public Use Microdata Sample) data off the Census FTP server and helps calculate estimates and margin of error.
  - Usage:
    ```python
    # %% Example Usage of PUMS functions
    import rwend_tools.pums as rp
    
    # Define the State, Year, and ACS Type to download
    state = 'CO' 
    year = 2022   
    acs_type = '1-Year'  
    
    # Grab PUMS data from Census FTP Server and read into Pandas
    df = rp.download_pums_data(state, year, acs_type)
    
    # Get the estimated number of males in the specified state/year
    # Compare result to the user verification file the census provides
    # Access the verification file here: https://www.census.gov/programs-surveys/acs/microdata/documentation.html
    # For Colorado in 2022, the User Verification file says:
        # Total Males: 2,961,075
        # MOE: 4,990
    
    estimate, margin_of_error = rp.est_moe_sdr(df[df['SEX']==1], 'Person')
    print('2022 ACS 1-Year, Estimated Total Males in CO: {:,.2f}'.format(estimate))
    print('Margin of Error: {:,.2f}'.format(margin_of_error))
    ```

### 2. custom_logging
  - This module helps create custom logging and email notifications
  - Prerequisites:
    - gmail_app_pwd needs to be set/defined as an environmental variable. This should be an app password you obtain from google if you want to use the email functionality of this module. Without this you can still use this to create log files but won't be able to send log files over email.
  - Usage:
    ```python
    import rwend_tools.custom_logging as rc
    import os
    
    # Set up email configuration 
    email_config = {
        'capacity': 100_000,
        'fromaddr': 'example_sender@gmail.com',
        'toaddr': 'example_recipient@gmail.com',
        'subject': 'Example Subject',
        'smtp_server': 'smtp.gmail.com',
        'smtp_port': 587,
        'login': 'example_sender@gmail.com',
        'password': os.environ['gmail_app_pwd']
    }
    
    # Initialize logger
    logger = rc.configure_logging(log_email=True, email_config=email_config)
    
    # Helps keep me organized, can track a log email to a scheduled run or a folder name that matches these
    process_id = '001'
    process_name = 'Test'
    
    subject_success = f'Success -- {process_id} -- {process_name} Ran'
    subject_error = f'Error -- {process_id} -- {process_name} Failed'
    
    # Set up one email for successful runs, one for if we have any errors
    # Only changing subject, but can have errors send to/from other emails if desired
    try:
        logger.info('First line of logging')
        logger.info('Second line of logging')
        logger.info('Third line of logging')
    
        rc.send_log_over_email(
            logger,
            fromaddr=email_config['fromaddr'],
            toaddr=email_config['toaddr'],
            subject=subject_success
        )
    except Exception as e:
        logger.error(f'Process failed with error: {e}')
        rc.send_log_over_email(
            logger,
            fromaddr=email_config['fromaddr'],
            toaddr=email_config['toaddr'],
            subject=subject_error
        )
    ```
