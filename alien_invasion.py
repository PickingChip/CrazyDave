import sys
from time import sleep
import pygame
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard


class AlienInvasion:
    """管理游戏资源和行为的类"""
    def __init__(self):
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self._create_fleet()
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)
        pygame.mixer.music.load('music/bgm.ogg')
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.play()
        self.play_button = Button(self, "Play")


    def _create_fleet(self):
        """创建一个目标群"""
        # 创建一个目标并计算一行可以容纳多少个对象
        # 目标之间的间距为其宽度
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2*alien_width)
        number_aliens_x = available_space_x // (2*alien_width)
        # 计算可容纳多少行目标
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - (2*alien_height) - ship_height)
        number_rows = available_space_y // (1 * alien_height)
        for row_number in range(int(number_rows)):
            # 创建第一行目标
            for alien_number in range(number_aliens_x):
                # 创建一个目标并加入其中
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height / 4 + 1.5 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _ship_hit(self):
        """响应被撞到"""
        if self.stats.ships_left > 0:
            # 将生命值减一
            self.stats.ships_left -= 1
            # 清空界面
            self.aliens.empty()
            self.bullets.empty()
            # 刷新界面
            self._create_fleet()
            self.ship.center_ship()
            # 暂停界面
            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _check_aliens_bottom(self):
        """检查是否有目标到达底部"""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # 像飞船被撞到一样处理
                self._ship_hit()
                break

    def _check_fleet_edges(self):
        """有目标到达边缘时采用相应的措施"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """将正群的目标下移，并改变他们的方向"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def run_game(self):
        """开始游戏主循环"""
        while True:
            self._check_events()
            if self.stats.game_active:

                self.ship.update()
                self._update_bullets()
                self._update_aliens()
            self._update_screen()

    def _update_bullets(self):
        # 更新子弹的位置
        self.bullets.update()
        # 删除消失的子弹
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        # 检查是否有子弹命中目标
        collections = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if collections:
            for aliens in collections.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()
        if not self.aliens:
            self.bullets.empty()
            self.settings.increase_speed()
            self._create_fleet()
            self.stats.level += 1
            self.sb.prep_level()


    def _update_aliens(self):
        """更新目标的位置"""
        self._check_fleet_edges()
        self.aliens.update()
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
        self._check_aliens_bottom()

    def _check_events(self):
        # 监视键盘和鼠标事件。
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        """在玩家单击Play按钮时开始新游戏"""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            # 重置游戏统计信息
            self.settings.initialize_dynamic_settings()
            self.stats.reset_stats()
            self.stats.game_active = True
            #清空剩下的界面
            self.aliens.empty()
            self.bullets.empty()
            # 创建新的界面
            self._create_fleet()
            self.ship.center_ship()
            pygame.mouse.set_visible(False)
            self.sb.prep_score()
            self.sb.prep_level()

    def _check_keydown_events(self, event):
        """响应按键"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_1:
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            self.settings.screen_width = self.screen.get_rect().width
            self.settings.screen_height = self.screen.get_rect().height
            self.ship = Ship(self)
        elif event.key == pygame.K_2:
            self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
            self.ship = Ship(self)

    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        """创建一颗子弹，并将其加入组编bullets中"""
        if len(self.bullets) <self.settings.bullet_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_screen(self):
        # 每次循环时屏幕都会重新设置
        #self.screen.fill(self.settings.bg_color)
        # 加载背景glass图片(目前的问题是加载图片会变卡)
        bg_image = pygame.image.load("images/glass.png")
        # 绘制背景图片
        self.screen.blit(bg_image, (0, 0))
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)
        self.sb.show_score()
        if not self.stats.game_active:
            self.play_button.draw_button()
        # 让最近绘制的屏幕可见。
        pygame.display.flip()


if __name__ == '__main__':
    # 创建游戏实例并运行
    ai = AlienInvasion()
    ai.run_game()



