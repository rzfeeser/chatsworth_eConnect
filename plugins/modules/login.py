#!/usr/bin/python

# Copyright: (c) 2018, Terry Jones <terry.jones@example.org>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
import requests # our module requires requests to be installed
from urllib3.exceptions import InsecureRequestWarning


from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: login

short_description: always run the login module first to grab a sessionid token

version_added: "1.0.0"

description: The login module will always be run at the top of a playbook so that the sessionid token can be grabbed.
This value is returned, and should be registered. Ex. register: results where results.sessionid has the token. Pass this token to all other modules.

options:
    ip:
        description: This is the IP of the device we want to connect to.
        required: true
        type: str
    username:
        description: This is the username on the device we want to connect to.
        required: true
        type: str
    password:
        description: This is the password on the device we want to connect to.
        required: true
        type: str

# Specify this value according to your collection
# in format of namespace.collection.doc_fragment_name
extends_documentation_fragment:
    - my_namespace.my_collection.my_doc_fragment_name

author:
    - Zach Feeser (@rzfeeser)
    - Dan 

'''

EXAMPLES = r'''
# Grab a sessionid token
- name: Test with a message
  rzfeeser.chatsworth_eConnect.login:
    username: admin
    password: larry123
    ip: 192.168.8.2
  register: results

- name: Display the sessionid token
  debug:
    var: results.sessionid
'''

RETURN = r'''
# These are examples of possible return values, and in general should use other names for return values.
sessionid:
    description: This is the token we are after
    type: str
    returned: always
    sample: '12ad3479876'
message:
    description: message related to response
    type: str
    returned: always
    sample: 'OK'
resultCode:
    description: A 0 indicates success (returned on JSON by HTTP request).
    type: int
    returned: always
    sample: 0
'''

from ansible.module_utils.basic import AnsibleModule


def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        username=dict(type='str', required=True),
        password=dict(type='str', required=True),
        ip=dict(type='str', required=True)
    )

    # seed the result dict in the object
    # we primarily care about changed and state
    # changed is if this module effectively modified the target
    # state will include any data that you want your module to pass back
    # for consumption, for example, in a subsequent task
    result = dict(
        changed=False,
        sessionid='',
        message='',
        resultCode=0
    )

    # the AnsibleModule object will be our abstraction working with Ansible
    # this includes instantiation, a couple of common attr would be the
    # args/params passed to the execution, as well as if the module
    # supports check mode
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    # if the user is working with this module in only check mode we do not
    # want to make any changes to the environment, just return the current
    # state with no modifications
    if module.check_mode:
        module.exit_json(**result)

    # manipulate or modify the state as needed (this is going to be the
    # part where your module will do what it needs to do)
    
    # creating a session
    s = requests.Session()

    cred = {'user': module.params['username'], 'password': module.params['password']}  # Creates JSON file for login credentials

    ## create our url
    url = f"https://{{ module.params['ip'] }}"

    res = s.post(url + '/bulk/login', json=cred, verify=False)  # Sends login POST.

    param = res.json()  # Converts response to JSON file.

 
    # seed the values into our result to send back to our user
    result['sessionid'] = param.get('sessionid')  # Finds value of session ID key in param file.
    result['message'] = param.get('message')
    result['resultCode'] = param.get['resultCode']

    # AnsibleModule.fail_json() to pass in the message and the result
    if result['resultCode'] != 0:
        module.fail_json(msg='Chatsworth eConnect Power PDU returned a non-zero runcode! (This is bad)', **result)

    # in the event of a successful module execution, you will want to
    # simple AnsibleModule.exit_json(), passing the key/value results
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
