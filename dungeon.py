# -*- coding: utf-8 -*-
import csv
import datetime
import json

import players_config as pc

REMAINING_TIME = '123456.0987654321'
FIELD_NAMES = ['current_location', 'current_experience', 'current_date']


class Dungeon:

    def __init__(self, dungeon_map, steps_log=None):
        self.dungeon_map = dungeon_map
        self.steps_log = steps_log
        self.location_actions = {}
        self.game_on = True
        self.started_at = datetime.datetime.now()
        self.time_passed = None
        self.start_location = None
        self.hero = None

    def open_map(self):
        with open(self.dungeon_map, "r") as dung_map:
            """ Collecting name of the first location in dungeon"""
            dungeon_map = json.load(dung_map)
            for key in dungeon_map.keys():
                start_location_name = key
            self.start_location = dungeon_map[start_location_name]

    def write_steps_log(self):
        with open(self.steps_log, 'a', newline='') as out_csv:
            writer = csv.writer(out_csv)
            writer.writerow(FIELD_NAMES)

    def restart_game(self):
        """
        Starting new game. Initializing new hero and starting time, also greetings users and tells them basic rules
        """
        self.started_at = datetime.datetime.now()
        print("Hello stranger!")
        print("Glad to see you again!")
        print("Are you ready to face the monsters in this cave and find out the exit?")
        print("Well, let`s see")
        print("There is only 1 way")
        print("You have to get at least 280 experience to open the hatch")
        print("Oh, almost forgot!")
        print(f"You have only {REMAINING_TIME} seconds to leave this cave, or ...")
        print("Good luck, Stranger!")
        print()
        self.hero = pc.Hero(REMAINING_TIME, start_location=self.start_location)

    def try_again(self):
        """
        Asking user if he wants to play again.
        Logging information about player`s last game
        :return: None
        """
        if self.steps_log:
            with open(csv_file, 'a', newline='') as out_csv:
                writer = csv.writer(out_csv)
                for line in self.hero.csv_snippet:
                    writer.writerow(line)
        try:
            restart = input("Try again?\n\t1. Yes\n\t2. No\n-> ")
            if restart.isdigit():
                restart = int(restart)
                if restart == 1:
                    self.restart_game()
                elif restart == 2:
                    self.game_on = False
            else:
                raise TypeError("Write an integer value")
        except TypeError:
            print('Try again')

    def current_location_info(self):
        """
        Collecting information about the location the player at.
        :return: None
        """

        self.time_passed = datetime.datetime.now() - self.started_at
        action_counter = 0
        print()
        print(f"You are at the location {self.hero.current_location_name}")
        print(f"You have {self.hero.current_xp} exp and {self.hero.remaining_time} second left before flood")
        print(f"Time passed {self.time_passed.seconds} seconds")
        print("You can see inside:")
        for item in self.hero.current_location:
            action_counter += 1
            if isinstance(item, str):
                track_name = item + 'id' + str(action_counter)
                if track_name in self.hero.killed_mobs:
                    continue
                else:
                    print(f"  - Mob {item}")
                    self.location_actions[action_counter] = {"actions": f"Fight mob {item}",
                                                             "hero_act": self.hero.mob_fight,
                                                             "action_param": [item, action_counter],
                                                             }
            if isinstance(item, dict):
                for key in item.keys():
                    print(f"  - Location {key}")
                    self.location_actions[action_counter] = \
                        {
                            "action_param": [key, self.hero.current_location[action_counter - 1]],
                            "actions": f"Move to {key}",
                            "hero_act": self.hero.move_to,
                            "console_out": item
                        }
        self.location_actions[0] = {"hero_act": self.try_again,
                                    "actions": "Surrender",
                                    }

    def current_location_actions(self):
        """ Iterating the dict with location information and shows to users their possible actions"""
        print()
        print("Choose action:")
        for num in self.location_actions.keys():
            possible_action = self.location_actions[num]["actions"]
            print(f"    {num}. {possible_action}")

    def player_choose_action(self, users_action):
        """
        Calling the correct heroes methods according to users choice
        :param users_action:
        :return: None
        """

        heroes_action = self.location_actions[users_action]
        print(f"You decided to {heroes_action['actions']}")
        heroes_action["hero_act"](heroes_action["action_param"])
        self.hero.current_date = datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')
        hero_info = [self.hero.current_location_name, self.hero.current_xp, self.hero.current_date]
        self.hero.csv_snippet.append(hero_info)

    def run(self):
        self.open_map()
        if self.steps_log:
            self.write_steps_log()
        self.restart_game()
        while self.game_on:

            self.current_location_info()
            self.current_location_actions()

            try:
                users_action = input("-> ")
                if users_action.isdigit():
                    users_action = int(users_action)
                    if users_action == 0:
                        self.try_again()
                    else:
                        self.player_choose_action(users_action=users_action)
                else:
                    raise TypeError("Write an integer value")
            except KeyError:
                print("This action is not available.\nTry again")
            except ValueError:
                print("This action is not available.\nTry again")
            except TypeError:
                print("This action is not available.\nTry again")
            if self.hero.winner:
                print(f'Time passed {self.time_passed.seconds} seconds')
                self.try_again()
            if self.hero.is_dead:
                self.try_again()

            self.location_actions = {}


if __name__ == '__main__':
    csv_file = 'dungeon_logs.csv'
    dm = "rpg.json"
    dungeon_game = Dungeon(dungeon_map=dm, steps_log=csv_file)
    dungeon_game.run()