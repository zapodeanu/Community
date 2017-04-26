
# developed by Gabi Zapodeanu, TSA, GSS, Cisco Systems


# !/usr/bin/env python3

import requests
import json
import requests.packages.urllib3

from requests_toolbelt import MultipartEncoder
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)  # Disable insecure https warnings

from Spark_APIs_init import SPARK_AUTH, SPARK_URL

# declarations for team/room/membership

spark_team_name = 'TeamTest'
spark_room_name = 'RoomTest'
email = 'gabriel.zapodeanu@gmail.com'


def pprint(json_data):
    """
    Pretty print JSON formatted data
    :param json_data:
    :return:
    """

    print(json.dumps(json_data, indent=4, separators=(' , ', ' : ')))


def create_spark_team(team_name):
    """
    This function will create a Spark team with the title team_name
    Call to Spark - /teams
    :param team_name: new Spark team name
    :return: the Spark team id
    """

    payload = {'name': team_name}
    url = SPARK_URL + '/teams'
    header = {'content-type': 'application/json', 'authorization': SPARK_AUTH}
    team_response = requests.post(url, data=json.dumps(payload), headers=header, verify=False)
    team_json = team_response.json()
    team_id = team_json['id']
    return team_id


def get_spark_team_id(team_name):
    """
    This function will find a Spark team with the title team_name
    Call to Spark - /teams
    :param team_name: Spark team name
    :return: the Spark team id
    """

    team_id = None
    url = SPARK_URL + '/teams'
    header = {'content-type': 'application/json', 'authorization': SPARK_AUTH}
    team_response = requests.get(url, headers=header, verify=False)
    team_json = team_response.json()
    team_list = team_json['items']
    for teams in team_list:
        if teams['name'] == team_name:
            team_id = teams['id']
    return team_id


def create_spark_room(room_name, team_name):
    """
    This function will create a Spark room with the title room name, part of the team - team name
    Calls to: Find the Spark team_id by calling our function get_spark_team_id
              Call to Spark - /rooms, to create the new Room
    :param room_name: Spark room name
    :param team_name: Spark team name
    :return: the Spark room id
    """

    team_id = get_spark_team_id(team_name)
    payload = {'title': room_name, 'teamId': team_id}
    url = SPARK_URL + '/rooms'
    header = {'content-type': 'application/json', 'authorization': SPARK_AUTH}
    room_response = requests.post(url, data=json.dumps(payload), headers=header, verify=False)
    room_json = room_response.json()
    room_number = room_json['id']
    return room_number


def get_spark_room_id(room_name):
    """
    This function will find the Spark room id based on the room name
    Call to Spark - /rooms
    :param room_name: The Spark room name
    :return: the Spark room Id
    """

    payload = {'title': room_name}
    room_number = None
    url = SPARK_URL + '/rooms'
    header = {'content-type': 'application/json', 'authorization': SPARK_AUTH}
    room_response = requests.get(url, data=json.dumps(payload), headers=header, verify=False)
    room_list_json = room_response.json()
    room_list = room_list_json['items']
    for rooms in room_list:
        if rooms['title'] == room_name:
            room_number = rooms['id']
    return room_number


def add_spark_team_membership(team_name, email_invite):
    """
    This function will add membership to the Spark team with the team name
    Calls to: It will call first the function get_spark_team_id(team_name) to find out the team id
              Spark - /memberships to add membership
    Input:      team name and email address to invite, global variable - Spark auth access token
    Output:     none
    :param team_name: The Spark team name
    :param email_invite: Spark user email to add to the team
    :return:
    """

    team_id = get_spark_team_id(team_name)
    payload = {'teamId': team_id, 'personEmail': email_invite, 'isModerator': 'true'}
    url = SPARK_URL + '/team/memberships'
    header = {'content-type': 'application/json', 'authorization': SPARK_AUTH}
    membership_response = requests.post(url, data=json.dumps(payload), headers=header, verify=False)
    membership_json = membership_response.json()
    try:
        membership = membership_json['personEmail']
    except:
        membership = None
    return membership


def delete_spark_team(team_name):
    """
    This function will delete the Spark team with the team name
    Calls to: it will call first the function to find out the team id.
              Spark - /teams/ to find delete the team
    :param team_name: The Spark team name
    :return:
    """

    team_id = get_spark_team_id(team_name)
    url = SPARK_URL + '/teams/' + team_id
    header = {'content-type': 'application/json', 'authorization': SPARK_AUTH}
    requests.delete(url, headers=header, verify=False)
    print("Deleted Spark Team :  ", team_name)


def last_spark_room_message(room_name):
    """
    This function will find the last message from the Spark room with the {room_name}
    Call to function to find the room_id
    Followed by API call to /messages?roomId={room_id}
    :param room_name: the Spark room name
    :return: {last_message} - the text of the last message posted in the room
             {last_person_email} - the author of the last message in the room
    """

    room_id = get_spark_room_id(room_name)
    url = SPARK_URL + '/messages?roomId=' + room_id
    header = {'content-type': 'application/json', 'authorization': SPARK_AUTH}
    response = requests.get(url, headers=header, verify=False)
    list_messages_json = response.json()
    list_messages = list_messages_json['items']
    last_message = list_messages[0]['text']
    last_person_email = list_messages[0]['personEmail']
    return [last_message, last_person_email]


def post_spark_room_message(room_name, message):
    """
    This function will post the {message} to the Spark room with the {room_name}
    Call to function to find the room_id
    Followed by API call /messages
    :param room_name: the Spark room name
    :param message: the text of the message to be posted in the room
    :return: none
    """

    room_id = get_spark_room_id(room_name)
    payload = {'roomId': room_id, 'text': message}
    url = SPARK_URL + '/messages'
    header = {'content-type': 'application/json', 'authorization': SPARK_AUTH}
    requests.post(url, data=json.dumps(payload), headers=header, verify=False)
    print("Message posted :  ", message)


def post_spark_room_file(room_name, file_name, file_type, file_path):
    """
    This function will post the file with the name {file} to the Spark room with the {room_name}
    Call to function get_spark_room_id(room_name) to find the room_id
    Followed by API call /messages
    :param room_name: Spark room name
    :param file_name: File name to be uploaded
    :param file_type: File type
    :param file_path: File path local on the computer
    :return: 
    """

    room_id = get_spark_room_id(room_name)

    # get the file name without the extension
    file = file_name.split('.')[0]

    payload = {'roomId': room_id,
               'files': (file, open(file_path+file_name, 'rb'), file_type)
               }
    # encode the file info, example: https://developer.ciscospark.com/blog/blog-details-8129.html

    m = MultipartEncoder(fields=payload)
    url = SPARK_URL + '/messages'
    header = {'content-type': m.content_type, 'authorization': SPARK_AUTH}
    response = requests.post(url, data=m, headers=header, verify=False)

    print('File posted :  ', file_path+file_name)


def main():

    # check to see if the team exists, if it does not create the Spark team with the spark_team_name

    team_id = get_spark_team_id(spark_team_name)
    if team_id is None:
        team_id = create_spark_team(spark_team_name)
        print('Created ', spark_team_name, ' Team ID: ', team_id)
    else:
        print('Team found ', spark_team_name, ' Team ID: ', team_id)

    # check to see if the room exists, if not create a new room with the spark_team_name, part of the team with the spark_team_name

    room_id = get_spark_room_id(spark_room_name)
    if room_id is None:
        room_id = create_spark_room(spark_room_name, spark_team_name)
        print('Created ', spark_room_name, ' Room ID: ', room_id)
    else:
        print('Room found ', spark_room_name, ' Room ID: ', room_id)

    # invite new members to join the room

    membership_status = add_spark_team_membership(spark_team_name, email)
    if membership_status is None:
        print('Team member invitation failed')
    else:
        print('Team member ', email, ' invited to team ', spark_team_name)

    # Input the message

    spark_message = input('Please enter the Spark message: ')

    # Post a message in the Spark Room

    post_spark_room_message(spark_room_name, spark_message)

    # Find the last message posted in the room

    last_spark_message = last_spark_room_message(spark_room_name)[0]
    last_user_message = last_spark_room_message(spark_room_name)[1]

    print('The last message from the room ', spark_room_name, ' was: ', last_spark_message)
    print('The last message from the room ', spark_room_name, ' was posted by: ', last_user_message)

    file_name = 'SunPeaks.jpg'
    file_type = 'image/jpg'
    file_path = '/Users/gzapodea/PythonCode/Community/'

    post_spark_room_file(spark_room_name, file_name, file_type, file_path)

    # delete Spark team - optional step

    if input('Do you delete the Spark Team  - ' + spark_team_name + ' - ? (y/n)  ') == 'y':
        delete_spark_team(spark_team_name)


if __name__ == '__main__':
    main()
