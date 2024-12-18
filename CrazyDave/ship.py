import pygame


class Ship:
    """管理飞船的类"""

    def __init__(self, ai_game):
        """初始化飞船并设置其初始位置"""
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        # 加载飞船图像并获取其外接矩形
        self.image = pygame.image.load('images/ship.png')
        self.rect = self.image.get_rect()

        # 对于每艘飞船，都将其放在屏幕的底部的中央
        self.rect.midbottom = self.screen_rect.midbottom
        self.moving_right = False
        self.moving_left = False
        self.blow_up = False
        # 在飞船的属性中储存小数
        self.x = float(self.rect.x)

    def update(self):
        """根据移动标志调整对象的位置"""
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed
        self.rect.x = self.x

    def blitme(self):
        """在指定位置绘制飞船"""
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """让飞船显示在正中央"""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)


