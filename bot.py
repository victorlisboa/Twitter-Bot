import tweepy
from time import sleep
from random import choice
from mysql.connector import connection

def create_con():
    cnx = connection.MySQLConnection(user='bb9ec0ae9cfec0', password='68704f35',
                              host='us-cdbr-east-03.cleardb.com',
                              database='heroku_4039ed9669d1447',
                              use_pure=False)
    return cnx


# Autenticantion
consumer_key = ''
consumer_secret = ''
access_token = ''
access_token_secret = ''

keys = [consumer_key, consumer_secret, access_token, access_token_secret]

with open('API_info.txt') as f:
    text = f.readlines()
    for line in range(4):
        keys[line] = text[line].rstrip('\n')
consumer_key, consumer_secret, access_token, access_token_secret = [i for i in keys]

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

# Frases
frases = ['Você disse Itabuna??? A melhor cidade do mundo!? O paraíso brasileiro...',
          'Itabuna é simplesmente incrível! Lugar melhor nesse país não há.',
          'A capital do cacau... Itabuna é realmente tudo, não é mesmo?',
          '"Merces Laborum Suorum", do latim: "A recompensa de seus trabalhos" é o lema dessa cidade maravilhosa',
          'Itabocas, grande metrópole do sul baiano.',
          'A famosa cidade da pedra preta!',
          'Hoje é um belo dia pra aproveitar essa cidade passeando na beira-rio.',
          'Você sabia que Jorge Amado, grande escritor brasileiro, nasceu em Itabuna? Essa cidade é tudo de bom!',
          'A terra grapiúna é a mais bela dos arredores!',
          ]

def store_last_seen_id(last_seen_id, op):
    '''Escreve o último ID visto no arquivo correspondente.'''
    if op == 'reply':
        cnx = create_con()
        cursor = cnx.cursor()
        cursor.execute("SELECT * FROM IDs")
        cursor.fetchall()
        cursor.execute(f"UPDATE IDs SET ID_REPLY = {last_seen_id} WHERE nome = 'IDs'")
        cursor.close()
        cnx.close()
        print(last_seen_id)
    elif op == 'rt':
        cnx = create_con()
        cursor = cnx.cursor()
        cursor.execute("SELECT * FROM IDs")
        cursor.fetchall()
        cursor.execute(f"UPDATE IDs SET ID_RT = {last_seen_id} WHERE nome = 'IDs'")
        cursor.close()
        cnx.close()
        print(last_seen_id)


def get_last_seen_id(op):
    '''Recupera o último ID visto'''
    cnx = create_con()
    cursor = cnx.cursor()

    if op == 'reply':
        cursor.execute("SELECT * FROM IDs")
        id = cursor.fetchall()
        print(id+'REPLY')
        cursor.close()
        cnx.close()
        return id[0][0]
    elif op == 'rt':
        cursor.execute("SELECT * FROM IDs")
        id = cursor.fetchall()
        print(id+'RT')
        cursor.close()
        cnx.close()
        return id[0][1]
    
def reply_to_tweets():
    last_seen_id_reply = get_last_seen_id('reply')
    mentions = api.mentions_timeline(last_seen_id_reply, tweet_mode = 'extended')  # O argumento da função é o id do ponto de partida
    
    for mention in reversed(mentions):  # reversed garante que as ações serão realizadas do tweet mais recente ao mais antigo.
        last_seen_id_reply = mention.id
        if 'itabuna' in mention.full_text.lower() or 'itabocas' in mention.full_text.lower():
            try:
                api.create_favorite(mention.id)
            except:
                pass
            api.update_status(\
                f'@{mention.author.screen_name} {choice(frases)}',
                last_seen_id_reply)  # Responde o tweet com esta string
            
            print(f'@{mention.author.screen_name} {choice(frases)}') # Monitoramento no terminal

    store_last_seen_id(last_seen_id_reply, 'reply')  # Salva o último ID visto

def retweet():
    last_seen_id_rt = get_last_seen_id('rt')
    searches = api.search('(Itabuna OR Itabocas)', result_type = 'recent', since_id = last_seen_id_rt)

    for search in reversed(searches):
        last_seen_id_rt = search.id
        flag = False
        if 'itabuna' in search.text.lower() or 'itabocas' in search.text.lower()\
        and search.author.screen_name != 'itabuner':  # Se tem itabuna no tweet e ele não é meu
            try:
                if search.entities['urls'][0]['expanded_url'][8:15] == 'twitter':
                    flag = True
            except:
                if search.entities['urls'] == []:
                    flag = True
            if flag:
                try:
                    api.retweet(search.id)
                except:
                    pass
            
            print(search.text.lower())  # Monitoramento no terminal
            
    store_last_seen_id(last_seen_id_rt, 'rt')


while True:
    retweet()
    reply_to_tweets()
    sleep(15)

