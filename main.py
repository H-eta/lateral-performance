# http://127.0.0.1:5001

from flask import Flask, render_template, request, request, redirect, url_for, session
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import io
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

app = Flask(__name__)
app.secret_key = os.urandom(24)  # This generates a random 24-byte key


# Questions grouped by theme
questions_by_theme = {
    'Vida e desempenho': [
        {'question': 'Satisfação com a Vida', 'options': ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'], 'option_points': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 'total_question_points': 0, "type": "single", 'index': 1, 'page': 1, 'has_idk_option': False, 'required': True, 'explanation': None, 'is_scale': True},
        {'question': 'Desempenho Profissional', 'options': ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'], 'option_points': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 'total_question_points': 0, "type": "single", 'index': 2, 'page': 1, 'has_idk_option': False, 'required': True, 'explanation': None, 'is_scale': True},
    ],
    'Principal': [
        {'question': 'Sinto-me vivo(a) activo(a).', 'options': ['Concordo Plenamente', 'Concordo', 'Neutro', 'Discordo', 'Discordo Totalmente'], 'option_points': [0, 0, 0, 0, 0], 'total_question_points': 0, "type": "single", 'index': 3, 'page': 2, 'has_idk_option': False, 'required': True, 'explanation': None, 'is_scale': False},
        {'question': 'A minha vida interessa-me e entusiasma-me.', 'options': ['Concordo Plenamente', 'Concordo', 'Neutro', 'Discordo', 'Discordo Totalmente'], 'option_points': [0, 0, 0, 0, 0], 'total_question_points': 0, "type": "single", 'index': 4, 'page': 2, 'has_idk_option': False, 'required': True, 'explanation': None, 'is_scale': False},
        {'question': 'Sinto-me satisfeito(a) com as minhas relações pessoais.', 'options': ['Concordo Plenamente', 'Concordo', 'Neutro', 'Discordo', 'Discordo Totalmente'], 'option_points': [0, 0, 0, 0, 0], 'total_question_points': 0, "type": "single", 'index': 5, 'page': 2, 'has_idk_option': False, 'required': True, 'explanation': None, 'is_scale': False},
        {'question': 'Sinto que a minha vida está a ter um impacto positivo nas pessoas que me rodeiam.', 'options': ['Concordo Plenamente', 'Concordo', 'Neutro', 'Discordo', 'Discordo Totalmente'], 'option_points': [0, 0, 0, 0, 0], 'total_question_points': 0, "type": "single", 'index': 6, 'page': 2, 'has_idk_option': False, 'required': True, 'explanation': None, 'is_scale': False},
        {'question': 'Sinto que a minha vida tem um propósito e um significado.', 'options': ['Concordo Plenamente', 'Concordo', 'Neutro', 'Discordo', 'Discordo Totalmente'], 'option_points': [0, 0, 0, 0, 0], 'total_question_points': 0, "type": "single", 'index': 7, 'page': 2, 'has_idk_option': False, 'required': True, 'explanation': None, 'is_scale': False},
        {'question': 'Tenho um sistema de valores e crenças que orientam as minhas actividades quotidianas.', 'options': ['Concordo Plenamente', 'Concordo', 'Neutro', 'Discordo', 'Discordo Totalmente'], 'option_points': [0, 0, 0, 0, 0], 'total_question_points': 0, "type": "single", 'index': 8, 'page': 2, 'has_idk_option': False, 'required': True, 'explanation': None, 'is_scale': False},
        {'question': 'Sinto que estou a fazer progressos em direcção aos meus objectivos.', 'options': ['Concordo Plenamente', 'Concordo', 'Neutro', 'Discordo', 'Discordo Totalmente'], 'option_points': [0, 0, 0, 0, 0], 'total_question_points': 0, "type": "single", 'index': 9, 'page': 2, 'has_idk_option': False, 'required': True, 'explanation': None, 'is_scale': False},
        {'question': 'Sou capaz de gerir e equilibrar bem as minhas diferentes funções e responsabilidades.', 'options': ['Concordo Plenamente', 'Concordo', 'Neutro', 'Discordo', 'Discordo Totalmente'], 'option_points': [0, 0, 0, 0, 0], 'total_question_points': 0, "type": "single", 'index': 10, 'page': 2, 'has_idk_option': False, 'required': True, 'explanation': None, 'is_scale': False},
        {'question': 'Sinto que tenho controlo sobre a minha vida.', 'options': ['Concordo Plenamente', 'Concordo', 'Neutro', 'Discordo', 'Discordo Totalmente'], 'option_points': [0, 0, 0, 0, 0], 'total_question_points': 0, "type": "single", 'index': 11, 'page': 2, 'has_idk_option': False, 'required': True, 'explanation': None, 'is_scale': False},
    ],
    'Exercício': [
        {'question': 'A minha quantidade média de exercício de resistência de intensidade moderada por semana é de:', 'options': ['Menos de 30 min', '30 a 70 min', '70 a 110 min', '110 a 150 min', 'Mais de 150 min', 'Não sei'], 'option_points': [1, 2, 3, 4, 5, 0], 'total_question_points': 0, "type": "single", 'index': 12, 'page': 3, 'has_idk_option': True, 'required': True, 'explanation': '(por ex., caminhada rápida, corrida lenta, etc.)', 'is_scale': False},
        {'question': 'A minha quantidade média de exercício vigoroso por semana é de:', 'options': ['Menos de 20 min', '20 a 40 min', '40 a 60 min', '60 a 75 min', 'Mais de 75 min', 'Não sei'], 'option_points': [1, 2, 3, 4, 5, 0], 'total_question_points': 0, "type": "single", 'index': 13, 'page': 3, 'has_idk_option': True, 'required': True, 'explanation': '(por ex., treinos de alta intensidade, jogos, etc.)', 'is_scale': False},
        {'question': 'Faço algum tipo de treino de força.', 'options': ['Nunca', '1 a 2 dias por mês', '1 dia por semana', '2 dias por semana', 'Pelo menos, 3 dias por semana', 'Não sei'], 'option_points': [1, 2, 3, 4, 5, 0], 'total_question_points': 0, "type": "single", 'index': 14, 'page': 3, 'has_idk_option': True, 'required': True, 'explanation': '(isto inclui exercícios com o peso do corpo, máquinas ou pesos)', 'is_scale': False},
        {'question': 'A minha contagem diária de passos é, em média', 'options': ['Menos de 3 000', 'Entre 3 000 a 5 000', 'Entre 5 000 a 7 000', 'Entre 7 000 a 10 000', 'Mais de 10 000', 'Não sei'], 'option_points': [1, 2, 3, 4, 5, 0], 'total_question_points': 0, "type": "single", 'index': 15, 'page': 3, 'has_idk_option': True, 'required': True, 'explanation': None, 'is_scale': False},
        {'question': 'O meu volume de treino/exercício por semana é de', 'options': ['Menos de 1h', 'Entre 1 a 2h', 'Entre 2 a 4h', 'Entre 4 a 6h', 'Mais de 6h', 'Não sei'], 'option_points': [1, 2, 3, 4, 5, 0], 'total_question_points': 0, "type": "single", 'index': 16, 'page': 3, 'has_idk_option': True, 'required': True, 'explanation': None, 'is_scale': False},
        {'question': 'A minha frequência semanal de treino de agilidade é de', 'options': ['Não faço', '1 vez por mês', '2 vezes por mês', '1 vez por semana', '2 vezes por semana', 'Mais de 2 vezes por semana', 'Não sei'], 'option_points': [0, 1, 2, 3, 4, 5, 0], 'total_question_points': 0, "type": "single", 'index': 17, 'page': 3, 'has_idk_option': True, 'required': True, 'explanation': None, 'is_scale': False},
        {'question': 'A minha frequência semanal de treino de equilíbrio é de', 'options': ['Não faço', '1 vez por mês', '2 vezes por mês', '1 vez por semana', '2 vezes por semana', 'Mais de 2 vezes por semana', 'Não sei'], 'option_points': [0, 1, 2, 3, 4, 5, 0], 'total_question_points': 0, "type": "single", 'index': 18, 'page': 3, 'has_idk_option': True, 'required': True, 'explanation': None, 'is_scale': False},
        {'question': 'A minha frequência semanal de treino de tempo de reacção é de', 'options': ['Não faço', '1 vez por mês', '2 vezes por mês', '1 vez por semana', '2 vezes por semana', 'Mais de 2 vezes por semana', 'Não sei'], 'option_points': [0, 1, 2, 3, 4, 5, 0], 'total_question_points': 0, "type": "single", 'index': 19, 'page': 3, 'has_idk_option': True, 'required': True, 'explanation': None, 'is_scale': False},
    ],
    'Biomecânica': [
        {'question': 'Sou capaz de fazer actividades quotidianas e exercício sem dor, desconforto nem limitações.', 'options': ['Concordo Plenamente', 'Concordo', 'Neutro', 'Discordo', 'Discordo Totalmente', 'Não sei'], 'option_points': [5, 4, 3, 2, 1, 0], 'total_question_points': 0, "type": "single", 'index': 20, 'page': 4, 'has_idk_option': True, 'required': True, 'explanation': None, 'is_scale': False},
        {'question': 'Sinto desconforto físico relacionado com a ergonomia durante o trabalho.', 'options': ['Constantemente', 'Frequentemente', 'Ocasionalmente', 'Raramente', 'Nunca', 'Não sei'], 'option_points': [1, 2, 3, 4, 5, 0], 'total_question_points': 0, "type": "single", 'index': 21, 'page': 4, 'has_idk_option': True, 'required': True, 'explanation': None, 'is_scale': False},
        {'question': 'Sinto desconforto físico relacionado com a ergonomia durante o sono.', 'options': ['Constantemente', 'Frequentemente', 'Ocasionalmente', 'Raramente', 'Nunca', 'Não sei'], 'option_points': [1, 2, 3, 4, 5, 0], 'total_question_points': 0, "type": "single", 'index': 22, 'page': 4, 'has_idk_option': True, 'required': True, 'explanation': None, 'is_scale': False},
        {'question': 'Sofro de dores nas costas e/ou pescoço.', 'options': ['Constantemente', 'Frequentemente', 'Ocasionalmente', 'Raramente', 'Nunca', 'Não sei'], 'option_points': [1, 2, 3, 4, 5, 0], 'total_question_points': 0, "type": "single", 'index': 23, 'page': 4, 'has_idk_option': True, 'required': True, 'explanation': None, 'is_scale': False},
        {'question': 'Faço exercícios que desenvolvem a minha mobilidade e flexibilidade.', 'options': ['Nunca', '1 vez por semana', '2 vezes por semana', '3 vezes por semana', 'Mais de 3 vezes por semana', 'Não sei'], 'option_points': [1, 2, 3, 4, 5, 0], 'total_question_points': 0, "type": "single", 'index': 24, 'page': 4, 'has_idk_option': True, 'required': True, 'explanation': None, 'is_scale': False},
        {'question': 'Na posição de pé e com as pernas completamente estendidas, consigo tocar com os dedos das mãos', 'options': ['Nos joelhos', 'A meio da perna', 'Nos tornozelos', 'Nos dedos dos pés', 'No chão', 'Não sei'], 'option_points': [1, 2, 3, 4, 5, 0], 'total_question_points': 0, "type": "single", 'index': 25, 'page': 4, 'has_idk_option': True, 'required': True, 'explanation': None, 'is_scale': False},
        {'question': 'Num dia de semana normal, estou sentado(a), em média', 'options': ['Mais de 14h', '12 a 14h', '10 a 12h', '8 a 10h', 'Menos de 8h', 'Não sei'], 'option_points': [1, 2, 3, 4, 5, 0], 'total_question_points': 0, "type": "single", 'index': 26, 'page': 4, 'has_idk_option': True, 'required': True, 'explanation': '(No trabalho, em casa, nas deslocações, etc)', 'is_scale': False},
        {'question': 'Tenho, com alguma frequência, dores nas seguintes partes do corpo', 'options': ['Tornozelos', 'Joelhos', 'Ancas', 'Ombros', 'Pulsos', 'Não tenho dores em nenhuma das partes acima mencionadas'], 'option_points': [-1, -1, -1, -1, -1, 0], 'total_question_points': 5, "type": "multiple", 'index': 27, 'page': 4, 'has_idk_option': False, 'required': True, 'explanation': None, 'is_scale': False},
    ],
    'Sono': [
        {'question': 'Deito-me diariamente à mesma hora.', 'options': ['Concordo Plenamente', 'Concordo', 'Neutro', 'Discordo', 'Discordo Totalmente', 'Não sei'], 'option_points': [5, 4, 3, 2, 1, 0], 'total_question_points': 0, "type": "single", 'index': 28, 'page': 5, 'has_idk_option': True, 'required': True, 'explanation': '(oscilações inferiores a 1h)', 'is_scale': False},
        {'question': 'Levanto-me diariamente à mesma hora.', 'options': ['Concordo Plenamente', 'Concordo', 'Neutro', 'Discordo', 'Discordo Totalmente', 'Não sei'], 'option_points': [5, 4, 3, 2, 1, 0], 'total_question_points': 0, "type": "single", 'index': 29, 'page': 5, 'has_idk_option': True, 'required': True, 'explanation': '(oscilações inferiores a 1h)', 'is_scale': False},
        {'question': 'Tenho e aplico diariamente uma rotina de relaxamento antes de me deitar.', 'options': ['Concordo Plenamente', 'Concordo', 'Neutro', 'Discordo', 'Discordo Totalmente', 'Não sei'], 'option_points': [5, 4, 3, 2, 1, 0], 'total_question_points': 0, "type": "single", 'index': 30, 'page': 5, 'has_idk_option': True, 'required': True, 'explanation': None, 'is_scale': False},
        {'question': 'A qualidade do meu sono é muito boa sem tomar qualquer tipo de estimulante/medicação.', 'options': ['Concordo Plenamente', 'Concordo', 'Neutro', 'Discordo', 'Discordo Totalmente', 'Não sei'], 'option_points': [5, 4, 3, 2, 1, 0], 'total_question_points': 0, "type": "single", 'index': 31, 'page': 5, 'has_idk_option': True, 'required': True, 'explanation': None, 'is_scale': False},
        {'question': 'A minha média de horas de sono durante os dias de trabalho é', 'options': ['Menos de 5h', '5 a 6h', '6 a 7h', '7 a 8h', 'Mais de 8h', 'Não sei'], 'option_points': [1, 2, 3, 4, 5, 0], 'total_question_points': 0, "type": "single", 'index': 32, 'page': 5, 'has_idk_option': True, 'required': True, 'explanation': None, 'is_scale': False},
        {'question': 'Sou capaz de trabalhar a um nível óptimo até às 12h sem beber café ou tomar qualquer outro tipo de estimulante.', 'options': ['Concordo Plenamente', 'Concordo', 'Neutro', 'Discordo', 'Discordo Totalmente', 'Não sei'], 'option_points': [5, 4, 3, 2, 1, 0], 'total_question_points': 0, "type": "single", 'index': 33, 'page': 5, 'has_idk_option': True, 'required': True, 'explanation': None, 'is_scale': False},
        {'question': 'Após as 13h, habitualmente, bebo café ou outro estimulante', 'options': ['Mais de 3 vezes', '3 vezes', '2 vezes', '1 vez', 'Não bebo', 'Não sei'], 'option_points': [1, 2, 3, 4, 5, 0], 'total_question_points': 0, "type": "single", 'index': 34, 'page': 5, 'has_idk_option': True, 'required': True, 'explanation': None, 'is_scale': False},
        {'question': 'Sofro de jetlag ou de fadiga geral relacionada com viagens.', 'options': ['Raramente ou nunca', 'De tempos a tempos', 'Mensalmente', 'Algumas vezes por mês', 'Várias vezes por mês', 'Não sei'], 'option_points': [5, 4, 3, 2, 1, 0], 'total_question_points': 0, "type": "single", 'index': 35, 'page': 5, 'has_idk_option': True, 'required': True, 'explanation': None, 'is_scale': False},
    ],
    'Nutrição': [
        {'question': 'As minhas escolhas alimentares ajudam-me a manter níveis de energia estáveis ao longo do dia.', 'options': ['Concordo Plenamente', 'Concordo', 'Neutro', 'Discordo', 'Discordo Totalmente', 'Não sei'], 'option_points': [5, 4, 3, 2, 1, 0], 'total_question_points': 0, "type": "single", 'index': 36, 'page': 6, 'has_idk_option': True, 'required': True, 'explanation': None, 'is_scale': False},
        {'question': 'Tenho um horário de refeições definido e cumpro-o diariamente.', 'options': ['Concordo Plenamente', 'Concordo', 'Neutro', 'Discordo', 'Discordo Totalmente', 'Não sei'], 'option_points': [5, 4, 3, 2, 1, 0], 'total_question_points': 0, "type": "single", 'index': 37, 'page': 6, 'has_idk_option': True, 'required': True, 'explanation': None, 'is_scale': False},
        {'question': 'A minha ingestão diária de água é, normalmente', 'options': ['0 a 0.5L', '0.5 a 1L', '1 a 1.5L', '1.5 a 2L', 'Mais de 2L', 'Não sei'], 'option_points': [1, 2, 3, 4, 5, 0], 'total_question_points': 0, "type": "single", 'index': 38, 'page': 6, 'has_idk_option': True, 'required': True, 'explanation': None, 'is_scale': False},
        {'question': 'O meu consumo semanal de álcool é, em média:', 'options': ['Mais de 20 unidades', '15 a 20 unidades', '10 a 14 unidades', '5 a 9 unidades', '0 a 4 unidades', 'Não sei'], 'option_points': [1, 2, 3, 4, 5, 0], 'total_question_points': 0, "type": "single", 'index': 39, 'page': 6, 'has_idk_option': True, 'required': True, 'explanation': '(1 unidade = 30ml de cerveja, 1/2 copo de vinho, uma medida de bebidas espirituosas)', 'is_scale': False},
        {'question': 'A minha ingestão diária de legumes e fruta é, normalmente', 'options': ['Menos de 2 porções', '2 a 3 porções', '4 a 5 porções', '6 a 7 porções', 'Pelo menos 8 porções', 'Não sei'], 'option_points': [1, 2, 3, 4, 5, 0], 'total_question_points': 0, "type": "single", 'index': 40, 'page': 6, 'has_idk_option': True, 'required': True, 'explanation': '(1 porção = 1 punhado)', 'is_scale': False},
        {'question': 'O meu consumo diário de alimentos e bebidas com elevado teor de açúcar é, normalmente', 'options': ['Pelo menos 4 porções', '3 porções', '2 porções', '1 porção', 'Menos de 1 porção', 'Não sei'], 'option_points': [1, 2, 3, 4, 5, 0], 'total_question_points': 0, "type": "single", 'index': 41, 'page': 6, 'has_idk_option': True, 'required': True, 'explanation': '(1 porção = 1 sumo ou refrigerante, 1 barra de chocolate, 1 bola de gelado, 1 fatia de bolo, 1 mão cheia de doces, etc)', 'is_scale': False},
        {'question': 'Estou satisfeito(a) com a percentagem da minha massa gorda', 'options': ['Concordo Plenamente', 'Concordo', 'Neutro', 'Discordo', 'Discordo Totalmente', 'Não sei'], 'option_points': [5, 4, 3, 2, 1, 0], 'total_question_points': 0, "type": "single", 'index': 42, 'page': 6, 'has_idk_option': True, 'required': True, 'explanation': None, 'is_scale': False},
        {'question': 'Estou satisfeito(a) com a minha massa corporal', 'options': ['Concordo Plenamente', 'Concordo', 'Neutro', 'Discordo', 'Discordo Totalmente', 'Não sei'], 'option_points': [5, 4, 3, 2, 1, 0], 'total_question_points': 0, "type": "single", 'index': 43, 'page': 6, 'has_idk_option': True, 'required': True, 'explanation': None, 'is_scale': False},
    ],
    'Energia': [
        {'question': 'Sinto-me com muita energia quando preciso.', 'options': ['Concordo Plenamente', 'Concordo', 'Neutro', 'Discordo', 'Discordo Totalmente', 'Não sei'], 'option_points': [5, 4, 3, 2, 1, 0], 'total_question_points': 0, "type": "single", 'index': 44, 'page': 7, 'has_idk_option': True, 'required': True, 'explanation': None, 'is_scale': False},
        {'question': 'Sinto-me descontraído quando preciso.', 'options': ['Concordo Plenamente', 'Concordo', 'Neutro', 'Discordo', 'Discordo Totalmente', 'Não sei'], 'option_points': [5, 4, 3, 2, 1, 0], 'total_question_points': 0, "type": "single", 'index': 45, 'page': 7, 'has_idk_option': True, 'required': True, 'explanation': None, 'is_scale': False},
        {'question': 'Sinto que transmito energia a quem me rodeia.', 'options': ['Concordo Plenamente', 'Concordo', 'Neutro', 'Discordo', 'Discordo Totalmente', 'Não sei'], 'option_points': [5, 4, 3, 2, 1, 0], 'total_question_points': 0, "type": "single", 'index': 46, 'page': 7, 'has_idk_option': True, 'required': True, 'explanation': None, 'is_scale': False},
        {'question': 'O meu trabalho dá-me energia e entusiasma-me.', 'options': ['Concordo Plenamente', 'Concordo', 'Neutro', 'Discordo', 'Discordo Totalmente', 'Não sei'], 'option_points': [5, 4, 3, 2, 1, 0], 'total_question_points': 0, "type": "single", 'index': 47, 'page': 7, 'has_idk_option': True, 'required': True, 'explanation': None, 'is_scale': False},
        {'question': 'Sou capaz de me concentrar no meu trabalho e evitar distracções ou alternar entre tarefas.', 'options': ['Concordo Plenamente', 'Concordo', 'Neutro', 'Discordo', 'Discordo Totalmente', 'Não sei'], 'option_points': [5, 4, 3, 2, 1, 0], 'total_question_points': 0, "type": "single", 'index': 48, 'page': 7, 'has_idk_option': True, 'required': True, 'explanation': None, 'is_scale': False},
        {'question': 'As pessoas com quem convivo transmitem-me energia.', 'options': ['Concordo Plenamente', 'Concordo', 'Neutro', 'Discordo', 'Discordo Totalmente', 'Não sei'], 'option_points': [5, 4, 3, 2, 1, 0], 'total_question_points': 0, "type": "single", 'index': 49, 'page': 7, 'has_idk_option': True, 'required': True, 'explanation': None, 'is_scale': False},
        {'question': 'Estou sempre preocupado(a) com alguma coisa.', 'options': ['Concordo Plenamente', 'Concordo', 'Neutro', 'Discordo', 'Discordo Totalmente', 'Não sei'], 'option_points': [1, 2, 3, 4, 5, 0], 'total_question_points': 0, "type": "single", 'index': 50, 'page': 7, 'has_idk_option': True, 'required': True, 'explanation': None, 'is_scale': False},
        {'question': 'Sinto, frequentemente, necessidade de recorrer a alimentos para ganhar energia.', 'options': ['Concordo Plenamente', 'Concordo', 'Neutro', 'Discordo', 'Discordo Totalmente', 'Não sei'], 'option_points': [1, 2, 3, 4, 5, 0], 'total_question_points': 0, "type": "single", 'index': 51, 'page': 7, 'has_idk_option': True, 'required': True, 'explanation': None, 'is_scale': False},
    ],
    'Saúde': [
        {'question': 'No que toca ao Colesterol, os meus níveis de LDL estão', 'options': ['Inferiores a 100', 'Entre 100 e 129', 'Entre 130 e 159', 'Entre 160 e 189', 'Acima de 190', 'Não sei'], 'option_points': [5, 4, 3, 2, 1, 0], 'total_question_points': 0, "type": "single", 'index': 52, 'page': 8, 'has_idk_option': True, 'required': True, 'explanation': None, 'is_scale': False},
        {'question': 'Os níveis dos meus triglicerídeos encontram-se', 'options': ['Acima dos 500', 'Entre os 301 e os 500', 'Entre os 201 e os 300', 'Entre os 150 e os 200', 'Abaixo dos 150', 'Não sei'], 'option_points': [1, 2, 3, 4, 5, 0], 'total_question_points': 0, "type": "single", 'index': 53, 'page': 8, 'has_idk_option': True, 'required': True, 'explanation': None, 'is_scale': False},
        {'question': 'A minha pressão arterial encontra-se dentro dos valores considerados saudáveis.', 'options': ['Concordo Plenamente', 'Concordo', 'Neutro', 'Discordo', 'Discordo Totalmente', 'Não sei'], 'option_points': [5, 4, 3, 2, 1, 0], 'total_question_points': 0, "type": "single", 'index': 54, 'page': 8, 'has_idk_option': True, 'required': True, 'explanation': None, 'is_scale': False},
        {'question': 'Tomo medicação para', 'options': ['Diabetes', 'Pressão arterial', 'Sono', 'Colesterol', 'Outro', 'Não tomo'], 'option_points': [-1, -1, -1, -1, -1, 0], 'total_question_points': 5, "type": "multiple", 'index': 55, 'page': 8, 'has_idk_option': False, 'required': True, 'explanation': None, 'is_scale': False},
        {'question': 'Fumo ou consumo produtos de tabaco', 'options': ['Diariamente', 'Vários dias por semana', 'Semanalmente', 'Raramente', 'Nunca'], 'option_points': [1, 2, 3, 4, 5], 'total_question_points': 0, "type": "single", 'index': 56, 'page': 8, 'has_idk_option': False, 'required': True, 'explanation': None, 'is_scale': False},
        {'question': 'Faltei ao trabalho por motivo de doença ou trabalhei doente nos últimos 6 meses', 'options': ['Mais de 15 dias', '12 a 15 dias', '8 a 11 dias', '4 a 7 dias', '0 a 3 dias', 'Não sei'], 'option_points': [1, 2, 3, 4, 5, 0], 'total_question_points': 0, "type": "single", 'index': 57, 'page': 8, 'has_idk_option': True, 'required': True, 'explanation': None, 'is_scale': False},
        {'question': 'Vou ao dentista com a regularidade de', 'options': ['Não fui nos últimos 5 anos', 'A última vez que fui foi há mais de 2 anos', 'A última vez que fui foi há mais de 1 ano', 'Vou 1 vez por ano', 'Vou 2 vezes por ano', 'Não sei'], 'option_points': [1, 2, 3, 4, 5, 0], 'total_question_points': 0, "type": "single", 'index': 58, 'page': 8, 'has_idk_option': True, 'required': True, 'explanation': None, 'is_scale': False},
        {'question': 'Fiz análises ao sangue', 'options': ['Há mais de 10 anos', 'Há mais de 5 anos', 'Há mais de 3 anos', 'Há mais de 1 ano', 'Faço todos os anos', 'Não sei'], 'option_points': [1, 2, 3, 4, 5, 0], 'total_question_points': 0, "type": "single", 'index': 59, 'page': 8, 'has_idk_option': True, 'required': True, 'explanation': None, 'is_scale': False},
    ],
    'Neuroplasticidade': [
        {'question': 'Sinto apoio por parte das pessoas com quem trabalho.', 'options': ['Concordo Plenamente', 'Concordo', 'Neutro', 'Discordo', 'Discordo Totalmente', 'Não sei'], 'option_points': [5, 4, 3, 2, 1, 0], 'total_question_points': 0, "type": "single", 'index': 60, 'page': 9, 'has_idk_option': True, 'required': True, 'explanation': None, 'is_scale': False},
        {'question': 'Sinto-me realizado no meu trabalho.', 'options': ['Concordo Plenamente', 'Concordo', 'Neutro', 'Discordo', 'Discordo Totalmente', 'Não sei'], 'option_points': [5, 4, 3, 2, 1, 0], 'total_question_points': 0, "type": "single", 'index': 61, 'page': 9, 'has_idk_option': True, 'required': True, 'explanation': None, 'is_scale': False},
        {'question': 'Tenho liberdade para realizar o meu trabalho de forma que entendo ser a melhor.', 'options': ['Concordo Plenamente', 'Concordo', 'Neutro', 'Discordo', 'Discordo Totalmente', 'Não sei'], 'option_points': [5, 4, 3, 2, 1, 0], 'total_question_points': 0, "type": "single", 'index': 62, 'page': 9, 'has_idk_option': True, 'required': True, 'explanation': None, 'is_scale': False},
        {'question': 'Incluo desafios/aprendizagens na minha rotina semanal.', 'options': ['Concordo Plenamente', 'Concordo', 'Neutro', 'Discordo', 'Discordo Totalmente', 'Não sei'], 'option_points': [5, 4, 3, 2, 1, 0], 'total_question_points': 0, "type": "single", 'index': 63, 'page': 9, 'has_idk_option': True, 'required': True, 'explanation': None, 'is_scale': False},
        {'question': 'Semanalmente, dedico aos meus desafios/aprendizagens', 'options': ['Não dedico tempo para desafios/aprendizagens', 'Menos de 30 min', 'Entre 30 a 60 min', 'Entre 1 a 3h', 'Mais de 3h', 'Não sei'], 'option_points': [1, 2, 3, 4, 5, 0], 'total_question_points': 0, "type": "single", 'index': 64, 'page': 9, 'has_idk_option': True, 'required': True, 'explanation': None, 'is_scale': False},
        {'question': 'Continuo a aprender com o passar do tempo.', 'options': ['Concordo Plenamente', 'Concordo', 'Neutro', 'Discordo', 'Discordo Totalmente', 'Não sei'], 'option_points': [5, 4, 3, 2, 1, 0], 'total_question_points': 0, "type": "single", 'index': 65, 'page': 9, 'has_idk_option': True, 'required': True, 'explanation': None, 'is_scale': False},
        {'question': 'Sinto-me valorizado pelas pessoas de quem mais gosto.', 'options': ['Concordo Plenamente', 'Concordo', 'Neutro', 'Discordo', 'Discordo Totalmente', 'Não sei'], 'option_points': [5, 4, 3, 2, 1, 0], 'total_question_points': 0, "type": "single", 'index': 66, 'page': 9, 'has_idk_option': True, 'required': True, 'explanation': None, 'is_scale': False},
        {'question': 'Passo tempo suficiente com as pessoas de quem mais gosto.', 'options': ['Concordo Plenamente', 'Concordo', 'Neutro', 'Discordo', 'Discordo Totalmente', 'Não sei'], 'option_points': [5, 4, 3, 2, 1, 0], 'total_question_points': 0, "type": "single", 'index': 67, 'page': 9, 'has_idk_option': True, 'required': True, 'explanation': None, 'is_scale': False},
    ],
    'Tempo': [
        {'question': 'Chego ao final da semana e fiz tudo o que queria e que precisava.', 'options': ['Concordo Plenamente', 'Concordo', 'Neutro', 'Discordo', 'Discordo Totalmente', 'Não sei'], 'option_points': [5, 4, 3, 2, 1, 0], 'total_question_points': 0, "type": "single", 'index': 68, 'page': 10, 'has_idk_option': True, 'required': True, 'explanation': None, 'is_scale': False},
        {'question': 'Sinto que tenho total controlo sobre a gestão do meu tempo.', 'options': ['Concordo Plenamente', 'Concordo', 'Neutro', 'Discordo', 'Discordo Totalmente', 'Não sei'], 'option_points': [5, 4, 3, 2, 1, 0], 'total_question_points': 0, "type": "single", 'index': 69, 'page': 10, 'has_idk_option': True, 'required': True, 'explanation': None, 'is_scale': False},
        {'question': 'Tenho as minhas prioridades bem definidas.', 'options': ['Concordo Plenamente', 'Concordo', 'Neutro', 'Discordo', 'Discordo Totalmente', 'Não sei'], 'option_points': [5, 4, 3, 2, 1, 0], 'total_question_points': 0, "type": "single", 'index': 70, 'page': 10, 'has_idk_option': True, 'required': True, 'explanation': None, 'is_scale': False},
        {'question': 'Tenho os papéis que desempenho na minha vida bem definidos.', 'options': ['Concordo Plenamente', 'Concordo', 'Neutro', 'Discordo', 'Discordo Totalmente', 'Não sei'], 'option_points': [5, 4, 3, 2, 1, 0], 'total_question_points': 0, "type": "single", 'index': 71, 'page': 10, 'has_idk_option': True, 'required': True, 'explanation': None, 'is_scale': False},
        {'question': 'Chego ao final da minha semana com a clara certeza de que desempenho todos os meus papéis de forma equilibrada.', 'options': ['Concordo Plenamente', 'Concordo', 'Neutro', 'Discordo', 'Discordo Totalmente', 'Não sei'], 'option_points': [5, 4, 3, 2, 1, 0], 'total_question_points': 0, "type": "single", 'index': 72, 'page': 10, 'has_idk_option': True, 'required': True, 'explanation': None, 'is_scale': False},
        {'question': 'Tenho tempo para cuidar de mim durante o meu tempo livre.', 'options': ['Concordo Plenamente', 'Concordo', 'Neutro', 'Discordo', 'Discordo Totalmente', 'Não sei'], 'option_points': [5, 4, 3, 2, 1, 0], 'total_question_points': 0, "type": "single", 'index': 73, 'page': 10, 'has_idk_option': True, 'required': True, 'explanation': None, 'is_scale': False},
        {'question': 'Estou satisfeito(a) com a forma como utilizo o meu tempo no trabalho.', 'options': ['Concordo Plenamente', 'Concordo', 'Neutro', 'Discordo', 'Discordo Totalmente', 'Não sei'], 'option_points': [5, 4, 3, 2, 1, 0], 'total_question_points': 0, "type": "single", 'index': 74, 'page': 10, 'has_idk_option': True, 'required': True, 'explanation': None, 'is_scale': False},
        {'question': 'Tenho tempo para realizar as actividades de que gosto.', 'options': ['Concordo Plenamente', 'Concordo', 'Neutro', 'Discordo', 'Discordo Totalmente', 'Não sei'], 'option_points': [5, 4, 3, 2, 1, 0], 'total_question_points': 0, "type": "single", 'index': 75, 'page': 10, 'has_idk_option': True, 'required': True, 'explanation': None, 'is_scale': False},
    ],
    'Bem-Estar no trabalho': [
        {'question': 'O meu trabalho entusiasma-me.', 'options': ['Concordo Plenamente', 'Concordo', 'Neutro', 'Discordo', 'Discordo Totalmente'], 'option_points': [0, 0, 0, 0, 0], 'total_question_points': 0, "type": "single", 'index': 76, 'page': 11, 'has_idk_option': False, 'required': True, 'explanation': None, 'is_scale': False},
        {'question': 'A maior parte dos dias, sinto-me realizado(a) no trabalho.', 'options': ['Concordo Plenamente', 'Concordo', 'Neutro', 'Discordo', 'Discordo Totalmente'], 'option_points': [0, 0, 0, 0, 0], 'total_question_points': 0, "type": "single", 'index': 77, 'page': 11, 'has_idk_option': False, 'required': True, 'explanation': None, 'is_scale': False},
        {'question': 'O trabalho que faço neste emprego é importante para mim.', 'options': ['Concordo Plenamente', 'Concordo', 'Neutro', 'Discordo', 'Discordo Totalmente'], 'option_points': [0, 0, 0, 0, 0], 'total_question_points': 0, "type": "single", 'index': 78, 'page': 11, 'has_idk_option': False, 'required': True, 'explanation': None, 'is_scale': False},
        {'question': 'Sinto-me livre para fazer o meu trabalho de forma que penso ser a melhor maneira de o fazer.', 'options': ['Concordo Plenamente', 'Concordo', 'Neutro', 'Discordo', 'Discordo Totalmente'], 'option_points': [0, 0, 0, 0, 0], 'total_question_points': 0, "type": "single", 'index': 79, 'page': 11, 'has_idk_option': False, 'required': True, 'explanation': None, 'is_scale': False},
        {'question': 'No trabalho, há pessoas que me compreendem verdadeiramente.', 'options': ['Concordo Plenamente', 'Concordo', 'Neutro', 'Discordo', 'Discordo Totalmente'], 'option_points': [0, 0, 0, 0, 0], 'total_question_points': 0, "type": "single", 'index': 80, 'page': 11, 'has_idk_option': False, 'required': True, 'explanation': None, 'is_scale': False},
        {'question': 'Tenho energia e bom humor.', 'options': ['Concordo Plenamente', 'Concordo', 'Neutro', 'Discordo', 'Discordo Totalmente'], 'option_points': [0, 0, 0, 0, 0], 'total_question_points': 0, "type": "single", 'index': 81, 'page': 11, 'has_idk_option': False, 'required': True, 'explanation': None, 'is_scale': False},
        {'question': 'Sinto-me fisicamente esgotado(a).', 'options': ['Concordo Plenamente', 'Concordo', 'Neutro', 'Discordo', 'Discordo Totalmente'], 'option_points': [0, 0, 0, 0, 0], 'total_question_points': 0, "type": "single", 'index': 82, 'page': 11, 'has_idk_option': False, 'required': True, 'explanation': None, 'is_scale': False},
        {'question': 'Sinto que não estou a pensar com clareza.', 'options': ['Concordo Plenamente', 'Concordo', 'Neutro', 'Discordo', 'Discordo Totalmente'], 'option_points': [0, 0, 0, 0, 0], 'total_question_points': 0, "type": "single", 'index': 83, 'page': 11, 'has_idk_option': False, 'required': True, 'explanation': None, 'is_scale': False},
        {'question': 'Sinto que não sou capaz de investir emocionalmente nos colegas de trabalho e nos clientes.', 'options': ['Concordo Plenamente', 'Concordo', 'Neutro', 'Discordo', 'Discordo Totalmente'], 'option_points': [0, 0, 0, 0, 0], 'total_question_points': 0, "type": "single", 'index': 84, 'page': 11, 'has_idk_option': False, 'required': True, 'explanation': None, 'is_scale': False},
    ],
    'Objetivo e motivação': [
        {'question': 'Como classificaria a sua necessidade ou urgência de mudar alguns dos seus comportamentos relacionados com o bem-estar?', 'options': ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'], 'option_points': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 'total_question_points': 0, "type": "single", 'index': 85, 'page': 12, 'has_idk_option': False, 'required': True, 'explanation': None, 'is_scale': True},
        {'question': 'Como classificaria a sua motivação para mudar alguns dos seus comportamentos relacionados com o bem-estar?', 'options': ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'], 'option_points': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 'total_question_points': 0, "type": "single", 'index': 86, 'page': 12, 'has_idk_option': False, 'required': True, 'explanation': None, 'is_scale': True},
        {'question': 'Como classificaria as suas actuais capacidades e conhecimentos relacionados com a melhoria da sua saúde e bem-estar?', 'options': ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'], 'option_points': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 'total_question_points': 0, "type": "single", 'index': 87, 'page': 12, 'has_idk_option': False, 'required': True, 'explanation': None, 'is_scale': True},
        {'question': 'Em que medida considera que o seu ambiente social e físico facilita a melhoria da sua saúde e bem-estar?', 'options': ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'], 'option_points': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 'total_question_points': 0, "type": "single", 'index': 88, 'page': 12, 'has_idk_option': False, 'required': True, 'explanation': None, 'is_scale': True},
    ],
}

# Phrases grouped by theme, matching the themes in questions
phrases_by_theme = {
    'Vida e Desempenho': [ ],
    'Principal': ['A Essência é a sua identidade, propósito e controlo na vida. Trata-se de encontrar um sentido, maximizar o seu potencial construir uma vida à sua semelhança.',],
    'Saúde': ['A saúde geral é o seu estado de saúde global. Esse mesmo estado de saúde geral reflecte-se na sua capacidade de recuperar e gerir doenças e, principalmente, preveni-las.',],
    'Exercício': ['A actividade física é uma combinação de treinos de capacidades motoras e coordenativas cujos estímulos promovem uma melhoria na qualidade de vida com vista a uma maior e melhor longevidade.', ],
    'Nutrição': ['A nutrição é a alimentação saudável que o(a) ajuda a estar no seu melhor, prevenir doenças e aumentar a imunidade.  Uma boa adaptação alimentar aos desafios diários sabendo o que comer, quando comer e como comer irá ajudar consideravelmente a manter o seu equilíbrio no que toca à sua composição corporal e energia física e mental.', ],
    'Sono': ['O sono é fundamental na sua capacidade de recuperar, regenerar e voltar a funcionar no dia seguinte. Todos os órgãos do corpo humano são influenciados, positiva ou negativamente, pela qualidade e quantidade do nosso sono.', ],
    'Biomecânica': ['A Biomecânica é a capacidade de o corpo se mover correctamente e com controlo. Para além disso, é fundamental, quer na execuções de movimentos quer em posições estácticas viver sem dor e sem limitações. Uma boa Biomecânica reduz o risco de lesões e permite uma actividade física mais eficaz e equilibrada ao longo da vida.', ],
    'Energia': ['A energia mental e física diz respeito à forma como gere os pensamentos, as emoções, a concentração, … É a sua capacidade de gerir o seu quotidiano do qual fazem parte o trabalho, a pressão, as relações e as prioridades, de forma a sentir-se enérgico e descontraído de acordo com as necessidades de cada contexto.', ],
    'Neuroplasticidade': ['A Neuroplasticidade refere-se aos estímulos que damos ao nosso cérebro e que irão contribuir para o seu desenvolvimento. Para além do Exercício e da Nutrição, o Amor, as relações Sociais e os Desafios, são parte integrante dos alicerces da Neuroplasticidade.', ],
    'Tempo': ['A Gestão do Tempo, mais do que gerirmos o nosso relógio, calendário ou compromissos, passa muito mais por nos gerirmos a nós próprios nos papéis que desempenhamos na nossa vida e aos quais damos valor.', ],
    'Bem-Estar no Trabalho': ['O clima da empresa em torno do bem-estar tem influência no seu bem-estar e desempenho a nível pessoal. Os temas desta secção incluem o compromisso, a realização, a aprendizagem, o propósito, a autonomia, as relações, a energia e a concentração.', ],
    'Objetivo e Motivação': ['Depois de ter respondido a estas perguntas, terá agora uma ideia um pouco melhor do seu bem-estar actual- Agora vamos tentar formular um objectivo inicial e avaliar a sua disponibilidade para a mudança.', ]

}

@app.route('/')
def home():
    session['first_visit'] = True
    return redirect(url_for('index', page_num=1))

@app.route('/page/<int:page_num>', methods=['GET', 'POST'])
def index(page_num=1):

    return render_template('index.html', questions_by_theme=questions_by_theme, phrases_by_theme=phrases_by_theme)

@app.route('/submit', methods=['POST'])
def submit():
    # Collect personal information from the form
    user_data = {
        'name': request.form['name'],
        'surname': request.form['surname'],
        'age': request.form['age'],
        'email': request.form['email'],
        'country': request.form['country'],
        'sex': request.form['sex'],
        'industry': request.form['industry'],
        'function': request.form['function'],
        'time_of_service': request.form['time_of_service']
    }

    # Collect all responses from the form
    #user_responses = {key: request.form.getlist(key) for key in request.form}
    user_responses = {key: request.form.getlist(key) for key in request.form if key not in user_data}
    user_responses = {k: list(set(v)) for k, v in user_responses.items()}



    # Store user_data in session for access during PDF generation
    session['user_data'] = user_data


    # Count "I don't know" responses
    idk_count = count_idk_answers(user_responses)

    theme_totals = calculate_question_points(user_responses, questions_by_theme)

    # Generate the PDF from the responses
    pdf_content = generate_pdf(user_responses, idk_count, theme_totals, user_data)

    # Send PDF as an email attachment
    send_email_with_attachment(pdf_content)

    return "PDF enviado com sucesso!"

def count_idk_answers(user_responses):
    idk_count = 0
    for question, answers in user_responses.items():
        for answer in answers:  # Iterate over the list of answers
            if answer.strip() == "Não sei":  # Case-sensitive comparison for "Não sei"
                idk_count += 1
    return idk_count


def calculate_question_points(responses, questions_by_theme):
    theme_totals = {theme: 0 for theme in questions_by_theme.keys()}
    total_questions_by_theme = {theme: len(questions) for theme, questions in questions_by_theme.items()}

    for theme, questions in questions_by_theme.items():
        for question in questions:
            question_index = question['index']

            # Collect all options for the specific question
            response_keys = [key for key in responses if f"question_{theme}_q{question_index}" in key]

            if response_keys:
                selected_options = []
                for response_key in response_keys:
                    selected_option = responses[response_key]
                    # Each selected option is added to the list
                    if isinstance(selected_option, str):
                        selected_option = [selected_option]
                    selected_options.extend(selected_option)  # Adding the selected options to the list

                # Removing duplicates to ensure each option is counted once
                selected_options = list(set(selected_options))


                question_total_points = question['total_question_points']  # Start with base points

                if question['type'] == 'multiple':
                    # For multiple-choice, iterate through each selected option and add points
                    for option in selected_options:
                        try:
                            # The option is found in the options list
                            option_index = question['options'].index(option)
                            option_value = question['option_points'][option_index]
                            question_total_points += option_value  # Add points for selected option
                        except ValueError:
                            continue

                else:
                    # For single-choice questions, ensure only one option is selected
                    if len(selected_options) > 1:
                        continue

                    try:
                        selected_index = question['options'].index(selected_options[0])
                        points = question['option_points'][selected_index]
                        question_total_points += points
                    except ValueError:
                        continue

                # Add the question total points to the theme total
                theme_totals[theme] += question_total_points

    # Calculations to put it in 1 - 10 scale
    final_theme_values = {
        theme: (theme_totals[theme] / total_questions_by_theme[theme]) * 2
        for theme in questions_by_theme.keys()
    }
    return final_theme_values

def generate_pdf(responses, idk_count, theme_totals, user_data):
    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)

    # Set margins and page size
    width, height = letter
    margin = 50
    # Starting position for the first content
    y_position = height - margin - 50
    line_height = 12
    max_lines_per_page = int((height - 2 * margin) / line_height)

    # Add a header/title
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(100, y_position, "Questionnaire Results")
    y_position -= 40

    # Add the "I don't know" count
    pdf.setFont("Helvetica", 12)
    pdf.drawString(100, y_position, f"'I don't know' was selected {idk_count} times.")
    y_position -= 40

    # Add User Data (Personal Information)
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(100, y_position, "User Information:")
    y_position -= 20

    # Loop through the user_data dictionary
    for key, value in user_data.items():
        if y_position - line_height < margin:  # Check if space is available
            pdf.showPage()  # Create a new page if not enough space
            y_position = height - margin - 50  # Reset position at the top of the new page
        pdf.setFont("Helvetica", 12)
        pdf.drawString(100, y_position, f"{key}: {value}")
        y_position -= line_height

    # Add a section break for the questionnaire section
    if y_position - line_height < margin:
        pdf.showPage()  # Create a new page for the questions
        y_position = height - margin - 50
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(100, y_position, "Questionnaire Answers:")
    y_position -= 20

    # Loop over each question and answer
    pdf.setFont("Helvetica", 12)
    for question, answer in responses.items():
        if y_position - line_height * 2 < margin:  # Check if space is available for the question and answer
            pdf.showPage()  # Add a new page if not enough space
            y_position = height - margin - 50  # Reset position at the top of the new page
        pdf.drawString(100, y_position, f"Question: {question}")
        y_position -= line_height
        pdf.drawString(100, y_position, f"Selected Option: {answer}")
        y_position -= line_height * 2  # Space between questions

    # Add theme totals
    if y_position - line_height * 2 < margin:
        pdf.showPage()  # Start a new page if needed
        y_position = height - margin - 50
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(100, y_position, "Theme Totals:")
    y_position -= 20

    for theme, total in theme_totals.items():
        if y_position - line_height < margin:
            pdf.showPage()  # Create a new page if space is running out
            y_position = height - margin - 50
        pdf.setFont("Helvetica", 12)
        if total <= 2:
            pdf.drawString(100, y_position, f"{theme}: {total} points - Muito Fraco")
        elif total > 2 and total <= 4:
            pdf.drawString(100, y_position, f"{theme}: {total} points - Fraco")
        elif total > 4 and total <= 6:
            pdf.drawString(100, y_position, f"{theme}: {total} points - Razoável")
        elif total > 6 and total <= 8:
            pdf.drawString(100, y_position, f"{theme}: {total} points - Bom")
        elif total > 8 and total <= 10:
            pdf.drawString(100, y_position, f"{theme}: {total} points - Muito Bom")

        y_position -= line_height

    # Save the PDF content to the buffer
    pdf.save()
    buffer.seek(0)
    return buffer.getvalue()

def send_email_with_attachment(pdf_content):
    # Email configuration
    sender_email = 'demo.questionnaire.mail@gmail.com'
    sender_password = 'vrom drwu dfzz lczv'
    recipient_email = 'beatrizlagos0411@gmail.com'

    # Create message object
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = 'Questionnaire Response'

    # Add PDF attachment
    attachment = MIMEBase('application', 'octet-stream')
    attachment.set_payload(pdf_content)
    encoders.encode_base64(attachment)
    attachment.add_header('Content-Disposition', 'attachment', filename='questionnaire.pdf')
    msg.attach(attachment)

    # Connect to SMTP server and send email
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient_email, msg.as_string())

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
