import pygame
import random
import pygame.time
from player import Player
from enemy import Enemy
from databasemanager import DatabaseManager
from variables import Variables

class Game():

    def rulesInit(self, var):
        rule1 = "1. Введите имя персонажа и нажмите Enter."
        rule2 = "2. Управление персонажем на стрелочки."
        rule3 = "3. За отведенное время нужно есть мышей."
        rule4 = "4. Если съедите меньше тридцати, то проиграете."
        rule5 = "5. Больше двигайтесь."
        var.rule1_surface = var.font.render(rule1, True, (255, 255, 255))
        var.rule1_rect = pygame.Rect(170, 200, 500, 36)
        var.rule2_surface = var.font.render(rule2, True, (255, 255, 255))
        var.rule2_rect = pygame.Rect(170, 250, 500, 36)
        var.rule3_surface = var.font.render(rule3, True, (255, 255, 255))
        var.rule3_rect = pygame.Rect(170, 300, 500, 36)
        var.rule4_surface = var.font.render(rule4, True, (255, 255, 255))
        var.rule4_rect = pygame.Rect(170, 350, 500, 36)
        var.rule5_surface = var.font.render(rule5, True, (255, 255, 255))
        var.rule5_rect = pygame.Rect(170, 400, 500, 36)

    # Отображение результата
    def show_result_message(self, var, message, top_players):
        result_font = pygame.font.Font(None, 36)
        result_text = result_font.render(message, True, (255, 255, 255))
        result_rect = result_text.get_rect(center=(var.SCREEN_WIDTH // 2, var.SCREEN_HEIGHT // 2))  # Центрирование текста

        # Очистка экрана
        var.screen.fill((0, 0, 0))

        # Отображение сообщения на экране
        var.screen.blit(result_text, result_rect)

        # Отображение списка топ-5 игроков
        y_offset = result_rect.bottom + 20  # Начальная вертикальная позиция для списка игроков
        for rank, (player_name, player_score) in enumerate(top_players, start=1):
            player_text = result_font.render(f"{rank}. {player_name}: {player_score}", True, (255, 255, 255))
            player_rect = player_text.get_rect(center=(var.SCREEN_WIDTH // 2, y_offset))
            var.screen.blit(player_text, player_rect)
            y_offset += player_rect.height + 10  # Увеличиваем вертикальную позицию для следующего игрока

        # Обновление экрана
        pygame.display.flip()

        # Ждем, пока игрок не нажмет клавишу для начала новой игры
        waiting_for_key = True
        while waiting_for_key:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        waiting_for_key = False

    # Инициализация
    def initialize(self, var):

        var.SCREEN_WIDTH = 800
        var.SCREEN_HEIGHT = 600

        # Основной игровой цикл
        var.running = True
        var.clock = pygame.time.Clock()

        # Создание группы спрайтов для врагов
        var.enemies = pygame.sprite.Group()

        var.db_manager = DatabaseManager("scores.db")
        var.db_manager.connect()
        var.db_manager.create_scores_table() # Создание таблицы, если она не существует

        var.font = pygame.font.Font(None, 36)
        # Создание окна игры
        var.screen = pygame.display.set_mode((var.SCREEN_WIDTH, var.SCREEN_HEIGHT))
        pygame.display.set_caption("PyMy крысу")

        # Время начала игры (в миллисекундах)
        var.start_time = pygame.time.get_ticks()

        # Продолжительность игры (в миллисекундах)
        var.game_duration = 60000

        # Загрузка изображения заднего фона
        var.background = pygame.image.load("images/background.png")

        var.player = Player()

        var.score = 0
        var.game_over = False

        # Запрос имени пользователя
        var.text = "Введите имя"
        var.input_active = True  # Флаг активности поля ввода

    # Ожидание ввода имени
    def waitingForInput(self, var):

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if var.text.strip() != "":
                        var.input_active = False
                        var.spawn_enemies = True
                elif event.key == pygame.K_BACKSPACE:
                    var.text = var.text[:-1]
                else:
                    var.text += event.unicode

        # Очистка экрана
        var.screen.fill((0, 0, 0))

        # Отображение заднего фона
        var.screen.blit(var.background, (0, 0))

        # Отображение поля ввода имени
        var.text_surface = var.font.render(var.text, True, (255, 255, 255))
        var.input_rect = pygame.Rect(50, 50, 200, 36)  # Позиция и размер поля ввода
        pygame.draw.rect(var.screen, (255, 255, 255), var.input_rect, 2)
        var.screen.blit(var.text_surface, (var.input_rect.x + 5, var.input_rect.y + 5))

        # Отображение текста правил игры
        var.screen.blit(var.rule1_surface, var.rule1_rect)
        var.screen.blit(var.rule2_surface, var.rule2_rect)
        var.screen.blit(var.rule3_surface, var.rule3_rect)
        var.screen.blit(var.rule4_surface, var.rule4_rect)
        var.screen.blit(var.rule5_surface, var.rule5_rect)

        # Обновление дисплея
        pygame.display.flip()

        # Ограничение частоты обновления экрана
        var.clock.tick(60)

    # Основной цикл
    def run(self, var):
        
        var.current_time = pygame.time.get_ticks()  # Получение текущего времени

        # Оставшееся время в миллисекундах
        remaining_time = max(0, var.game_duration - (pygame.time.get_ticks() - var.start_time))

        # Преобразование времени в секунды
        remaining_seconds = remaining_time // 1000

        # Создание текстового объекта для отображения времени
        time_text = var.font.render(f"Time: {remaining_seconds} s", True, (255, 255, 255))
        time_rect = time_text.get_rect(topright=(var.SCREEN_WIDTH - 10, 10))  # Позиция времени в верхнем правом углу

        if var.game_over:
            var.enemies.empty()
            var.text = "Введите имя"  # Сброс поля ввода имени
            var.input_active = True  # Включение ввода имени
            var.game_over = False

        # Проверка завершения игры
        if var.current_time - var.start_time >= var.game_duration:
            if var.score >= 30:
                var.message = "Поздравляем! Вы выиграли!"
                var.db_manager.insert_score(var.text, var.score) # Вставка результата в базу данных
            else:
                var.message = "Игра окончена. Вы проиграли."

            # Получение топ-5 игроков
            top_players = var.db_manager.get_top_players()

            self.show_result_message(var, var.message, top_players)

            # Сброс счета и других переменных для начала новой игры
            var.score = 0
            var.player.rect.centerx = var.SCREEN_WIDTH // 2
            var.player.rect.bottom = var.SCREEN_HEIGHT - 10
            var.start_time = pygame.time.get_ticks()
            var.game_over = True

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                var.running = False

            if var.input_active:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        var.input_active = False
                    elif event.key == pygame.K_BACKSPACE:
                        var.text = var.text[:-1]
                    else:
                        var.text += event.unicode

            # Обработка клавиш для управления персонажем
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    var.player.move_left()
                elif event.key == pygame.K_RIGHT:
                    var.player.move_right()
                elif event.key == pygame.K_UP:
                    var.player.move_up()
                elif event.key == pygame.K_DOWN:
                    var.player.move_down()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    var.player.stop()
            
            # Создание новых врагов
            if not var.input_active and random.randrange(100) < 15:
                new_enemy = Enemy()
                var.enemies.add(new_enemy)  # Добавление врага в группу спрайтов

        # Обновление позиции персонажа и врага
        var.player.update()
        var.enemies.update()

        # Проверка столкновения с врагами
        hits = pygame.sprite.spritecollide(var.player, var.enemies, True)
            
        # Если есть столкновения, увеличьте счет и выведите его
        if hits:
            var.score += len(hits)
        
        # Очистка экрана
        var.screen.fill((0, 0, 0))

        # Отображение заднего фона
        var.screen.blit(var.background, (0, 0))

        # Отображение времени на экране
        var.screen.blit(time_text, time_rect)

        # Отображение персонажа на экране
        var.screen.blit(var.player.image, var.player.rect)

        # Отображение поля ввода имени
        var.text_surface = var.font.render(var.text, True, (255, 255, 255))
        var.input_rect = pygame.Rect(50, 50, 200, 36)  # Позиция и размер поля ввода
        pygame.draw.rect(var.screen, (255, 255, 255), var.input_rect, 2)
        var.screen.blit(var.text_surface, (var.input_rect.x + 5, var.input_rect.y + 5))

        # Отображение счета на экране
        score_text = var.font.render(f"Счет: {var.score}", True, (255, 255, 255))
        var.screen.blit(score_text, (10, 10))

        # Отображение врагов
        var.enemies.draw(var.screen)

        # Обновление дисплея
        pygame.display.flip()

        # Ограничение частоты обновления экрана
        var.clock.tick(60)