import unittest
from decimal import Decimal
from unittest.mock import Mock

import players_config as player


class DungeonTest(unittest.TestCase):

    def setUp(self) -> None:
        self.hero = player.Hero(remaining_time='4456.0987654321', start_location='')
        self.hatch = ["Hatch_tm156.098765432", 4]

    def test_mob_fight_mob(self):
        random_mob = ["Mob_exp20_tm456", 1]
        self.hero._enemy_info = Mock()

        self.hero.mob_fight(mob=random_mob)

        self.assertEqual(self.hero.killed_mobs, [(random_mob[0] + 'id' + str(random_mob[1]))])
        self.hero._enemy_info.assert_called_once()

    def test_mob_fight_boss(self):
        random_boss = ["Boss_exp100_tm1050", 3]
        self.hero._enemy_info = Mock()

        self.hero.mob_fight(mob=random_boss)

        self.assertEqual(self.hero.killed_mobs, [(random_boss[0] + 'id' + str(random_boss[1]))])
        self.hero._enemy_info.assert_called_once()

    def test_mob_fight_dead(self):
        random_deadly_mob = ["Mob_exp20_tm4856", 2]
        self.hero.dead = Mock()

        self.hero.mob_fight(mob=random_deadly_mob)

        self.hero.dead.assert_called_once()

    def test_enemy_info_init(self):
        enemy = ['', 10, 20]

        self.hero._enemy_info(enemy)

        self.assertEqual(self.hero.remaining_time, Decimal('4436.0987654321'))
        self.assertEqual(self.hero.current_xp, Decimal('10'))