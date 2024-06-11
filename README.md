# rwend-tools
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
│   └── utils.py
```

## Usage Guide
### 1. custom_logging
  - This module helps create custom logging and email notifications
  - Prerequisites:
    - gmail_app_pwd needs to be set/defined as an environmental variable. This should be an app password you obtain from google if you want to use the email functionality of this module.
  - Usage:
    ```python
    from rwend_tools.custom_logging import set_logging, send_log_over_email
    
    log_email = 'user.email@gmail.com'
    process_id = '001'
    process_name = 'Test'

    subject_success = f'Success -- {process_id} -- {process_name} Ran'
    subject_error   = f'Error -- {process_id} -- {process_name} Failed'
    
    logger = set_logging(log_console=False, log_email=True)
    logger.info('Test')
    
    try:
        logger.info(f'First line of logging')
        logger.info(f'Second line of logging')
        logger.info(f'Third line of logging')
    
        send_log_over_email(
            logger,
            fromaddr=log_email,
            toaddr=log_email,
            subject=subject_success
        )
    except Exception as e:
        logger.info(f'Process failed with error: {e}')
        send_log_over_email(
            logger,
            fromaddr=log_email,
            toaddr=log_email,
            subject=subject_error
        )
    ```
### 2. google_helpers
  - This module helps makes working with Google Cloud Platform easier.
  - Usage:
    ```python
    import rwend_tools.google_helpers as gh
    
    ```
### 3. utils
  - This module contains assorted functions 
  - Usage:
     ```python
      from rwend_tools.utils import html_tables_to_yaml
      
      input_path = 'sample_markdown.md'
      html_tables_to_yaml(input_path)
     ```
    
