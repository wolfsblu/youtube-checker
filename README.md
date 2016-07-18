# YouTube Checker

A handy tool for users who prefer the terminal.

## Setup

1. Install dependencies using  
`pip install -r requirements.txt`
1. Use Google API Console to create OAuth 2.0 credentials:
   1. Visit the [developer console](https://console.developers.google.com)
   1. Create a new project
   1. Open the [API Manager](https://console.developers.google.com/apis/)
   1. Enable *YouTube Data API v3*
   1. Go to [Credentials](https://console.developers.google.com/apis/credentials)
   1. Configure the OAuth consent screen and create *OAuth client ID* credentials 
   1. Use Application Type *Other* and provide a client name (e.g. *Python*)
   1. Confirm and download the generated credentials as JSON file
1. Store the file in the application folder as *client_secrets.json*
1. Launch the program using `./checker.py`
1. A browser window should open asking for confirmation

## Usage 

Use the checker to add your favourite YouTube channels  
`./checker.py -u LastWeekTonight add`

Remove a channel you're no longer interested in  
`./checker.py -u LastWeekTonight remove`

List the previously added channels  
`./checker.py list`

Check for new uploads from a specific channel  
`./checker.py -u LastWeekTonight check`

Check for new uploads from any previously added channel  
`./checker.py check`
