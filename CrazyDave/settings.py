import pygame

class Settings:
    """储存游戏中的所有设置"""
    def __init__(self):
        """初始化游戏中的静态设置"""
        # 屏幕设置
        self.alien_speed = None
        self.bullet_speed = None
        self.fleet_direction = None
        self.ship_speed = None
        self.screen_width = 1200
        self.screen_height = 794
        self.bg_color = (230, 230, 230)
        # 飞船设置
        self.ship_limit = 0
        # 子弹设置
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (235, 182, 41)
        self.bullet_allowed = 10
        # 外星人设置
        self.fleet_drop_speed = 10

        # 加快游戏的节奏
        self.speedup_scale = 1.5
        # 得分增长
        self.score_scale = 1.5
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """初始化随游戏进程变化的设置"""
        self.ship_speed = 3.0
        self.bullet_speed = 3.0
        self.alien_speed = 1.5
        # fleet_direction 为1表示向右移，为-1表示向左移。
        self.fleet_direction = 1
        self.alien_points = 50


    def increase_speed(self):
        """提高速度设置"""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)


