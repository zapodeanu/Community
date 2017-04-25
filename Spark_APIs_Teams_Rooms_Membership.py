# developed by Gabi Zapodeanu, TSA, GSS, Cisco Systems


# !/usr/bin/env python3

import requests
import json
import requests.packages.urllib3

from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)  # Disable insecure https warnings

from Spark_APIs_init import SPARK_AUTH, SPARK_URL


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
    print(team_response)
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


def main():

    # Input Spark Team name

    team_name = input('Please enter the team name: ')

    # Input Spark Room name

    room_name = input('Please enter the room name: ')

    # Input email address to invite to room

    email = input('Please enter email address to invite: ')

    # check to see if the team exists, if it does not create the Spark team with the team_name

    team_id = get_spark_team_id(team_name)
    if team_id is None:
        team_id = create_spark_team(team_name)
        print('Created ', team_name, ' Team ID: ', team_id)
    else:
        print('Team found ', team_name, ' Team ID: ', team_id)

    # check to see if the room exists, if not create a new room with the room_name, part of the team with the team_name

    room_id = get_spark_room_id(room_name)
    if room_id is None:
        room_id = create_spark_room(room_name, team_name)
        print('Created ', room_name, ' Room ID: ', room_id)
    else:
        print('Room found ', room_name, ' Room ID: ', room_id)

    # invite new members to join the room

    membership_status = add_spark_team_membership(team_name, email)
    if membership_status is None:
        print('Team member invitation failed')
    else:
        print('Team member ', email, ' invited to team ', team_name)

    # delete Spark team - optional step

    if input('Do you delete the Spark Team  - ' + team_name + ' - ? (y/n)  ') == 'y':
        delete_spark_team(team_name)


if __name__ == '__main__':
    main()
