# coding: utf-8
"""
Практическая задача на структуры данных: нужно провести симуляцию чемпионата.
На входе есть список команд. Его вы задаете сами. Далее, каждая команда должна
провести матч со всеми остальными командами. С помощью стандартного модуля
random вы определяете счет, с которым завершилась та или иная встреча.
В конце программы нужно напечатать итоговую таблицу чемпионата в порядке
занятых мест, колонки такие: место команды, название команды, кол-во побед,
кол-во поражений, кол-во ничейных результатов, сколько голов забито, сколько
пропущено, кол-во набранных очков. За победу команде начисляется 3 очка,
за ничью 1, за поражение 0. Также нужно иметь возможность запросить,
с каким счетом завершилась та или иная встреча между определенными командами.
Соответственно, при каждом запуске программы вы будете получать новую
финальную таблицу чемпионата.
"""
import random
import itertools
import operator
from prettytable import PrettyTable


class Team:
    def __init__(self, name):
        self.name = name  # название команды
        self.place = 0  # место команды
        self.score = 0  # кол-во набранных очков
        self.number_of_wins = 0  # число побед
        self.number_of_loses = 0  # число поражений
        self.number_of_dead_heats = 0  # число "ничьих"
        self.scored_goals = 0  # кол-во забитых голов
        self.goals_agains = 0  # кол-во пропущенных голов

    def __str__(self):
        return self.name


def get_championship_table(teams):
    '''
    Создание красивой таблицы по итогам чемпиона
    :param teams: список команд (список объекто класса Team)
    :param return: объект типа PrettyTable, таблица с результатами
    '''
    # создадим красивую таблицу результатов
    championship_table = PrettyTable()
    championship_table._set_field_names(
            ["Место", "Название", "Побед", "Поражений", "Ничья", "Забито",
             "Пропущено", "Очки"])

    # сортировка результатов чемпионала и присвоение мест
    teams.sort(key=operator.attrgetter('score'), reverse=True)
    for team in teams:
        championship_table.add_row([team.place, team.name, team.number_of_wins,
                                    team.number_of_loses,
                                    team.number_of_dead_heats,
                                    team.scored_goals, team.goals_agains,
                                    team.score])
    return championship_table


def get_information_about_match(team_name_1, team_name_2, results):
    '''
    Получить информацию о матче
    :param team_name_1: название команды
    :param team_name_2: название команды
    :param results: результаты чемпионата
    :param return: результаты матча, если таковой существует
    '''
    if (team_name_1, team_name_2) in results:
        score_1, score_2 = results.get((team_name_1, team_name_2))
    elif (team_name_2, team_name_1) in results:
        score_2, score_1 = results.get((team_name_2, team_name_1))

    if ('score_1' in locals()) and ('score_2' in locals()):
        return '{}:{}'.format(score_1, score_2)
    return 'Такого матча не существует'


def update_score(team, team_score, opponent_score, status):
    '''
    Обновление информации о команде in-place
    :param team: команда, объект типа Team
    :param team_score: счёт команды в текущем матче, int
    :param opponent_score: счёт команды-противника в текущем матче, int
    :param status: статуст команды в текущем матче, string
    :param return: empty
    '''
    if status == 'win':
        team.number_of_wins += 1
    elif status == 'lose':
        team.number_of_loses += 1
    elif status == 'dead_heat':
        team.number_of_dead_heats += 1

    team.score += {
        'win': 3,
        'lose': 0,
        'dead_heat': 1
    }[status]
    team.scored_goals += team_score
    team.goals_agains += opponent_score


def get_match(team_1, team_2):
    '''
    Проведение матча между двумя командами
    :param team_1: команда 1, тип Team
    :param team_2: команда 2, тип Team
    :param return: словарь вида: (название команды 1, название команды 2):
    (cчёт 1, счёт 2)
    '''
    score_1 = random.randint(0, 5)
    score_2 = random.randint(0, 5)

    if score_1 > score_2:
        status_1, status_2 = 'win', 'lose'
    elif score_1 < score_2:
        status_1, status_2 = 'lose', 'win'
    else:
        status_1 = status_2 = 'dead_heat'

    update_score(team_1, score_1, score_2, status_1)
    update_score(team_2, score_2, score_1, status_2)

    return {(team_1.name, team_2.name): (score_1, score_2)}


if __name__ == '__main__':
    # список с названиями команд
    names_of_teams = [
        'Спартак',
        'Зенит',
        'Реал Мадрид',
        'ЦСКА',
        'Манчестер Юнайтед',
        'Барселона',
        'Арсенал',
        'Челси',
        'Ливерпуль',
        'Локомотив'
    ]

    # создаём команды
    teams = [Team(name_of_team) for name_of_team in names_of_teams]

    # проводим матчи между командами
    championship_results = dict()
    for two_teams in itertools.combinations(teams, 2):
        championship_results.update(get_match(two_teams[0], two_teams[1]))

    # сортировка результатов чемпионала и присвоение мест (see TODO-list #3)
    teams.sort(key=operator.attrgetter('score'), reverse=True)
    for i, team in enumerate(teams):
        team.place = i + 1

    print(get_championship_table(teams))

    while True:
        answer = input('Узнать подробности о матче? (y/n): ')
        if answer.lower() in ['y', 'yes', 'д', 'да']:
            try:
                team_1, team_2 = input(
                    'Введите названия команд через запятую и пробел: ').split(
                    ', ')
            except ValueError:
                print('\tПроверьте правильность ввода запроса!')
            except Exception as ex:
                print('\tОй! Вы что-то сломали:')
                print(ex)
            else:
                print('\t', get_information_about_match(team_1, team_2,
                                                        championship_results))
        elif answer.lower() in ['n', 'no', 'н', 'нет']:
            break
        else:
            print('\tНекорректный ответ!')
