# -*- coding: utf-8 -*-
import datetime
import re
from decimal import Decimal

LOCATION_SNIPPET = r"Location_([A-z]*\d+)_tm(\d+[.]*[\d]*)"
MOB_SNIPPET = r"Mob_exp(\d+)_tm(\d+)"
BOSS_SNIPPET = r"Boss_exp(\d+)_tm(\d+)"
HATCH_SNIPPET = r"Hatch_tm(\d+[.]*[\d]*)"


class Hero:
    """ Class creates hero that can walk throw the dungeon """

    def __init__(self, remaining_time, start_location, exit_xp=280):
        """

        :param remaining_time: float number that shows player`s status: if it is > 0, game is on
        :param start_location: key name in json file(map) which shows players start position
        :param exit_xp: count of xp, player must have to open the hatch(wint the game)
        """

        self.remaining_time = Decimal(remaining_time)
        self.exit_xp = exit_xp
        self.current_xp = 0
        self.current_date = datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')
        self.current_location = start_location
        self.current_location_name = 'Location_0_tm0'
        self.csv_snippet = []
        self.killed_mobs = []
        self.winner = False
        self.is_dead = False

    def mob_fight(self, mob):
        """
        Method handles event when hero faces the mob
        :param mob: mob information, expected name(mob[0]) and id(mob[1])
        :return: None
        """
        mob_info = re.match(MOB_SNIPPET, mob[0])
        boss_info = re.match(BOSS_SNIPPET, mob[0])
        track_name = mob[0] + 'id' + str(mob[1])
        if mob_info:
            self._enemy_info(mob_info)
        elif boss_info:
            self._enemy_info(boss_info)
        if self.remaining_time < 0:
            self.dead()
        self.killed_mobs.append(track_name)

    def _enemy_info(self, enemy):
        self.remaining_time -= Decimal(enemy[2])
        self.current_xp += Decimal(enemy[1])

    def move_to(self, location, ):
        """
        Method handles event when hero moves to the next location
        :param location: location information, expected index of the location in json file(location[1])
                         and content(location[0])
        :return: None
        """
        location_info = re.match(LOCATION_SNIPPET, location[0])
        hatch_info = re.match(HATCH_SNIPPET, location[0])
        if location_info:
            self.remaining_time -= Decimal(location_info[2])
            self.current_location_name = location_info[0]
            self.current_location = location[1][location_info[0]]
        elif hatch_info:
            self.remaining_time -= Decimal(hatch_info[1])
            if (self.current_xp >= self.exit_xp) and (self.remaining_time >= 0):
                self.winner = True
                print("Congratulations, you have found a Hatch")
            else:
                print("You have found a Hatch, but it`s not enough")
                self.dead()
        if self.remaining_time < 0:
            self.dead()

    def dead(self):
        """
        Method that handles death of the hero
        :return: death call
        """
        self.is_dead = True
        print("Ahh, guess, it is time to die")
