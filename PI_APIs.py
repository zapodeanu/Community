
# developed by Gabi Zapodeanu, TSA, GSS, Cisco Systems

# !/usr/bin/env python3

import requests
import json
import time
import datetime
import requests.packages.urllib3

from requests.packages.urllib3.exceptions import InsecureRequestWarning
from requests.auth import HTTPBasicAuth  # for Basic Auth

from PI_APIs_init import PI_URL, PI_USER, PI_PASSW

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)  # Disable insecure https warnings

# The following declarations need to be updated based on your lab environment


PI_AUTH = HTTPBasicAuth(PI_USER, PI_PASSW)


def pprint(json_data):
    """
    Pretty print JSON formatted data
    :param json_data:
    :return:
    """

    print(json.dumps(json_data, indent=4, separators=(' , ', ' : ')))


def update_cli_template(vlan_id,remote_client,file):
    """
    This function will update an existing CLI template with the values to be used for deployment
    :param vlan_id: VLAN ID of the remote client
    :param remote_client: IP address for the remote client
    :param file: file that contains the CLI template
    :return: will save the file with the template to be deployed, with the name: upd_+{file}
    """
    file_in = open(file, 'r')
    file_out = open('upd_'+file, 'w')
    for line in file_in:
        line = line.replace('$VlanId',vlan_id)
        line = line.replace('$RemoteClient',remote_client)
        file_out.write(line)
        print(line)
    file_in.close()
    file_out.close()


def pi_get_device_id(device_name):
    """
    Find out the PI device Id using the device hostname
    Call to Prime Infrastructure - /webacs/api/v1/data/Devices, filtered using the Device Hostname
    :param device_name: device hostname
    :return: PI device Id
    """

    url = PI_URL + '/webacs/api/v1/data/Devices?deviceName=' + device_name
    header = {'content-type': 'application/json', 'accept': 'application/json'}
    response = requests.get(url, headers=header, verify=False, auth=PI_AUTH)
    device_id_json = response.json()
    device_id = device_id_json['queryResponse']['entityId'][0]['$']
    return device_id


def pi_deploy_cli_template(device_id, template_name, variable_value):
    """
    Deploy a template to a device through Job
    Call to Prime Infrastructure - /webacs/api/v1/op/cliTemplateConfiguration/deployTemplateThroughJob
    :param device_id: device Prime Infrastructure id
    :param template_name: PI template name
    :param variable_value: variables to send to template in JSON format
    :return: PI job name
    """

    param = {
        'cliTemplateCommand': {
            'targetDevices': {
                'targetDevice': {
                    'targetDeviceID': str(device_id),
                    'variableValues': {
                        'variableValue': variable_value
                    }
                }
            },
            'templateName': template_name
        }
    }
    url = PI_URL + '/webacs/api/v1/op/cliTemplateConfiguration/deployTemplateThroughJob'
    header = {'content-type': 'application/json', 'accept': 'application/json'}
    response = requests.put(url, data=json.dumps(param), headers=header, verify=False, auth=PI_AUTH)
    job_json = response.json()
    job_name = job_json['mgmtResponse']['cliTemplateCommandJobResult']['jobName']
    print('job name: ', job_name)
    return job_name


def pi_get_job_status(job_name):
    """
    Get job status in PI
    Call to Prime Infrastructure - /webacs/api/v1/data/JobSummary, filtered by the job name, will provide the job id
    A second call to /webacs/api/v1/data/JobSummary using the job id
    :param job_name: Prime Infrastructure job name
    :return: PI job status
    """

    #  find out the PI job id using the job name

    url = PI_URL + '/webacs/api/v1/data/JobSummary?jobName=' + job_name
    header = {'content-type': 'application/json', 'accept': 'application/json'}
    response = requests.get(url, headers=header, verify=False, auth=PI_AUTH)
    job_id_json = response.json()
    job_id = job_id_json['queryResponse']['entityId'][0]['$']

    #  find out the job status using the job id

    url = PI_URL + '/webacs/api/v1/data/JobSummary/' + job_id
    header = {'content-type': 'application/json', 'accept': 'application/json'}
    response = requests.get(url, headers=header, verify=False, auth=PI_AUTH)
    job_status_json = response.json()
    #  print(json.dumps(job_status_json, indent=4, separators=(' , ', ' : ')))
    job_status = job_status_json['queryResponse']['entity'][0]['jobSummaryDTO']['resultStatus']
    return job_status


def pi_delete_cli_template(cli_template_name):
    """
    This function will delete the PI CLI template with the name {cli_template_name}
    API call to /webacs/api/v1/op/cliTemplateConfiguration/deleteTemplate
    :param cli_template_name: the CLI template to be deleted
    :return: none
    """

    url = PI_URL + '/webacs/api/v1/op/cliTemplateConfiguration/deleteTemplate?templateName='+cli_template_name
    header = {'content-type': 'application/json', 'accept': 'application/json'}
    response = requests.delete(url, headers=header, verify=False, auth=PI_AUTH)
    if response.status_code == 200:
        print('PI CLI Template with the name: ', cli_template_name, ' deleted')
    else:
        print('PI CLI Template with the name: ', cli_template_name, ' not deleted')


def pi_update_cli_template(vlan_id,remote_client,file):
    """
    This function will update an existing CLI template with the values to be used for deployment
    :param vlan_id: VLAN ID of the remote client
    :param remote_client: IP address for the remote client
    :param file: file that contains the CLI template
    :return: will save the DATETIME+{file} file with the template to be deployed
    """
    file_in = open(file, 'r')
    file_out = open(CLI_DATE_TIME+file, 'w')
    for line in file_in:
        line = line.replace('$VlanId',vlan_id)
        line = line.replace('$RemoteClient',remote_client)
        file_out.write(line)
        print(line)
    file_in.close()
    file_out.close()


def pi_clone_cli_template(file):
    """
    This function will clone an existing CLI template with the name {file}. The new CLI template name will have
    the name DATETIME+{file}
    :param file: file that contains the CLI template
    :return: will save the DATETIME+{file} file with the template to be deployed
    """
    file_in = open(file, 'r')
    file_out = open(CLI_DATE_TIME+' '+file, 'w')
    for line in file_in:
        file_out.write(line)
    file_in.close()
    file_out.close()
    cloned_file_name = CLI_DATE_TIME+' '+file
    return cloned_file_name


def pi_post_cli_template(cli_file_name, cli_template):
    """
    This function will upload a new CLI template from the text file {cli_file_name}
    API call to /webacs/api/v1/op/cliTemplateConfiguration/upload
    :param cli_file_name: cli template text file
    :return:
    """
    cli_file = open(cli_file_name, 'r')
    cli_config = cli_file.read()
    param = {
        'cliTemplate': {
            'content': cli_config,
            'description': '',
            'deviceType': '',
            'name': cli_template,
            'path': '',
            'tags': '',
            'variables': ''
        },
        'version': ''
    }
    pprint(param)
    url = PI_URL + '/webacs/api/v1/op/cliTemplateConfiguration/upload'
    header = {'content-type': 'application/json', 'accept': 'application/json'}
    requests.post(url, json.dumps(param), headers=header, verify=False, auth=PI_AUTH)
    cli_file.close()




def get_job_status(job_name):
    """
    Get job status in PI
    Call to Prime Infrastructure - /webacs/api/v1/data/JobSummary, filtered by the job name, will provide the job id
    A second call to /webacs/api/v1/data/JobSummary using the job id
    :param job_name: Prime Infrastructure job name
    :return: PI job status
    """

    #  find out the PI job id using the job name

    url = PI_URL + '/webacs/api/v1/data/JobSummary?jobName=' + job_name
    header = {'content-type': 'application/json', 'accept': 'application/json'}
    response = requests.get(url, headers=header, verify=False, auth=PI_AUTH)
    job_id_json = response.json()
    job_id = job_id_json['queryResponse']['entityId'][0]['$']

    #  find out the job status using the job id

    url = PI_URL + '/webacs/api/v1/data/JobSummary/' + job_id
    header = {'content-type': 'application/json', 'accept': 'application/json'}
    response = requests.get(url, headers=header, verify=False, auth=PI_AUTH)
    job_status_json = response.json()
    #  print(json.dumps(job_status_json, indent=4, separators=(' , ', ' : ')))
    job_status = job_status_json['queryResponse']['entity'][0]['jobSummaryDTO']['resultStatus']
    return job_status


def main():

    global CLI_DATE_TIME
    DATE_TIME = str(datetime.datetime.now().replace(microsecond=0))

    # replace ":" with "-" from the Date and Time to meet the naming conventions for PI templates

    CLI_DATE_TIME = DATE_TIME.replace(':', '-')

    # client IP address - DNS lookup if available

    client_IP = '172.16.41.55'

    #  deploy DC router CLI template

    dc_device_hostname = 'PDX-RO'
    PI_dc_device_id = pi_get_device_id(dc_device_hostname)
    print('Head end router: ', dc_device_hostname, ', PI Device id: ', PI_dc_device_id)

    template_name = 'GREDConfig'
    variable_value = None    # the template does not require any variables
    PI_dc_job_name = pi_deploy_cli_template(PI_dc_device_id, template_name, variable_value)

    #  deploy remote router CLI template

    remote_device_hostname = client_connected[0]
    vlan_number = client_connected[2]
    print('Client connected to switch: ', remote_device_hostname, ' VLAN: ', vlan_number)
    PI_remote_device_id = pi_get_device_id(remote_device_hostname)
    print('Remote Router: ', remote_device_hostname, ', PI device Id: ', PI_remote_device_id)
    template_name = 'GRERConfig'
    variable_value = [
        {'name': 'RemoteClient', 'value': client_IP}, {'name': 'VlanId', 'value': str(vlan_number)}
    ]
    PI_remote_job_name = pi_deploy_cli_template(PI_remote_device_id, template_name, variable_value)

    # check for job status

    time.sleep(60)  #  time delay to allow PI de deploy the jobs
    dc_job_status = get_job_status(PI_dc_job_name)
    print('DC CLI template deployment status: ', dc_job_status)
    remote_job_status = get_job_status(PI_remote_job_name)
    print('Remote CLI template deployment status: ', remote_job_status)


if __name__ == '__main__':
    main()