# Ansible Collection - rzfeeser.chatsworth_eConnect
This collection is for Ansible automation of the Chatsworth PDU eConnect.

While leading a 5-day Ansible training event, I built this collection in response to a student's request to automate the Chatsworth PDU eConnect suite. They have a fairly well developed API, so writing the automation around it hasn't been to difficult. However, any and all feedback is appreciated.

For Ansible training for yourself, or your enterprise, contact sales@alta3.com.

# Installing Chatsworth eConnect Modules

### Step 1: Install the collection
- `ansible-galaxy collection install git+https://github.com/rzfeeser/chatsworth_eConnect.git`

### Step 2: Install python dependency `requests`
Currently, `requests` is required on the Ansible controller. If you're new to Python or Ansible, you can do your own research, however, `requests` is an unbelivably common 3rd party library. You can read about the project @ https://docs.python-requests.org/en/latest/

To install `requests`:
- `pip install requests`

In the future I would like to remove the requests dependency. I     don't see anything within the operations that couldn't be comple    ted by the standard library (urllib).

# Modules in the Collection
- login
    - The login module should be run (once) at the top of all playbooks. It returns the sessionid token that is required for authenticating with all other modules. Requires username and password.
- getconfig
    - Retrieve the PDU config data from /bulk/config. Requires sessionid token (see login moule).

# Chatsworth API documentation
https://www.chatsworth.com/en-us/documents/installation-instructions/econnect_pdu_api_user_manaul.pdf

# Special Thanks
- Dan 
