import os
import sys
import json
import requests

from gamemanager import GameManager
from utils.code_query import select_code
from utils.util_user_info_in_problem import update_user_info_in_problem
from utils.util_match import update_match_data
from userprogram import UserProgram


def match(match_data):
    match_dir = os.getcwd()     # os.path.join(os.getcwd(), 'match')
    extension = {'': '', 'C': '.c', 'C++': '.cpp', 'PYTHON': '.py', 'JAVA': '.java'}
    # update_url = 'http://127.0.0.1:8000/api/v1/game/' + match_data['match_id']

    challenger_code_filename = 'challenger{0}'.format(extension[match_data['challenger_language']])
    oppositer_code_filename = 'oppositer{0}'.format(extension[match_data['oppositer_language']])

    challenger_code_path = os.path.join(match_dir, challenger_code_filename)
    oppositer_code_path = os.path.join(match_dir, oppositer_code_filename)

    # challenger_code = select_code(match_data['challenger'], match_data['problem'])
    # oppositer_code = select_code(match_data['oppositer'], match_data['problem'])
    challenger_code = match_data['challenger_code']
    oppositer_code = match_data['oppositer_code']

    with open(challenger_code_path, 'w') as f:
        f.write(challenger_code)

    with open(oppositer_code_path, 'w') as f:
        f.write(oppositer_code)

    challenger = UserProgram(match_data['challenger'], match_data['challenger_language'], match_dir, challenger_code_filename)
    oppositer = UserProgram(match_data['oppositer'], match_data['oppositer_language'], match_dir, oppositer_code_filename)

    game_manager = GameManager(challenger=challenger, oppositer=oppositer,
                               placement_rule=match_data['placement'], action_rule=match_data['action'],
                               ending_rule=match_data['ending'], turn=match_data['turn'],
                               board_size=match_data['board_size'], board_info=match_data['board_info'],
                               obj_num=match_data['obj_num'])

    match_result, board_record, placement_record = game_manager.play_game()
    req = requests.put(update_url, data={'match_result':match_result, 'board_record':board_record, 'placement_record':placement_record})
    # with open('result.txt', 'w') as f:
    #     f.write(match_result)
    # with open('result.txt', 'a') as f:
    #     f.write(board_record)
    # with open('result.txt', 'a') as f:
    #     f.write(placement_record)

    #   update match data
    update_match_data(match_result, board_record, placement_record)


if __name__ == '__main__':
    # json_data = json.loads(sys.argv[1])

    with open('dummy_data2.json') as json_file:
        json_data = json.load(json_file)
    match(json_data)



