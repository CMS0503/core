import numpy as np
import os
import sys

from rules import Rules
from game_data import GameData
from excute_code import Execution


class GameManager:
    # ex) {placment_rule : [..., ..., ...]}
    def __init__(self, challenger, oppositer, placement_rule, action_rule, ending_rule, turn, board_size, board_info):
        self.board = np.zeros((board_size, board_size))
        
        self.challenger = challenger
        self.opposite = oppositer
        self.check_turn = turn

        self.game_data = GameData(placement_rule, action_rule, ending_rule, board_size, board_info)

        self.rules = Rules()
        self.execution = Execution()

        self.record = ''

        self.limit_time = 2000

    def play_game(self):
        user_turn = 0    # 0 : first player turn, 1 : later player turn
        total_turn = 0
        total_turn_limit = self.game_data.board_size ** 3
        is_ending = False
        result = ''

        self.compile_user_code()    # not finish

        #   make record folder, write initial board
        match_record_path = os.path.join(os.getcwd(), 'record')
        os.mkdir(match_record_path)
        with open(os.path.join(match_record_path, 'record.txt'), 'w') as f:
            f.write(self.board)

        while not is_ending:
            if total_turn > total_turn_limit:
                print("total_turn over")
                result = 'draw'
                return result

            #   user code execute
            user_placement = None
            if self.check_turn == 'challenger':
                user_placement = self.execution.execute_program(self.challenger.play, self.challenger.save_path)
                self.check_turn = 'oppositer'
            elif self.check_turn == 'oppositer':
                user_placement = self.execution.execute_program(self.opposite.play, self.opposite.save_path)
                self.check_turn = 'challenger'

            check_placement, new_board = self.rules.check_placment_rule(self.game_data, self.board, user_placement)
            if check_placement:
                self.board = new_board
                apply_action, new_board = self.rules.apply_action_rule(self.game_data, self.board)

                if apply_action:
                    self.board = new_board
                    self.add_data(check_placement, new_board)
                    check_ending = self.rules.check_ending(self.game_data, self.board)

                    if check_ending:
                        check_winner = self.rules.check_winner(self.game_data, self.board)




        return result

    def compile_user_code(self):
        pass

    def add_data(self, placement, board):

