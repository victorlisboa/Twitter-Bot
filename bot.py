import tweepy
from time import sleep
from random import choice
from mysql.connector import connection
import os

def create_con():
    '''Cria uma conexão com o banco de dados
       Creates a conextion to the data base'''
    cnx = connection.MySQLConnection(user=os.environ.get('user_bd'), password=os.environ.get('pass_bd'),
                              host=os.environ.get('host_bd'),
                              database=os.environ.get('db_bd'),
                              use_pure=False)
    return cnx

# Autenticação / Autenticantion
consumer_key = os.environ.get('consumer_key')
consumer_secret = os.environ.get('consumer_secret')
access_token = os.environ.get('access_token')
access_token_secret = os.environ.get('access_token_secret')

keys = [consumer_key, consumer_secret, access_token, access_token_secret]
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

# Frases / Sentences
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
    '''Escreve o último ID visto no arquivo correspondente.
       Writes last ID seen in the correspondent file.'''
    if op == 'reply':
        #print(last_seen_id, 'id que vai ser salvo replay')
        cnx = create_con()
        cursor = cnx.cursor()
        cursor.execute("SELECT * FROM IDs")
        cursor.fetchall()
        cursor.execute(f"UPDATE IDs SET ID_REPLY = {last_seen_id} WHERE nome = 'IDs'")
        cnx.commit()
        cursor.close()
        cnx.close()
    elif op == 'rt':
        #print(last_seen_id, 'id que vai ser salvo rt')
        cnx = create_con()
        cursor = cnx.cursor()
        cursor.execute("SELECT * FROM IDs")
        cursor.fetchall()
        cursor.execute(f"UPDATE IDs SET ID_RT = {last_seen_id} WHERE nome = 'IDs'")
        cnx.commit()
        cursor.close()
        cnx.close()


def get_last_seen_id(op):
    '''Pega o último ID visto.
       Gets last ID seen.'''
    cnx = create_con()
    cursor = cnx.cursor()

    if op == 'reply':
        cursor.execute("SELECT * FROM IDs")
        id = cursor.fetchall()
        #print(str(id[0][0])+'REPLY')
        cursor.close()
        cnx.close()
        return int(id[0][0])
    elif op == 'rt':
        cursor.execute("SELECT * FROM IDs")
        id = cursor.fetchall()
        #print(str(id[0][1])+'RT')
        cursor.close()
        cnx.close()
        return int(id[0][1])
    
def reply_to_tweets():
    last_seen_id_reply = get_last_seen_id('reply')
    #print(last_seen_id_reply)
    #print(type(last_seen_id_reply))
    mentions = api.mentions_timeline(last_seen_id_reply, tweet_mode = 'extended')  # O argumento da função é o id do ponto de partida
    
    for mention in reversed(mentions):  # reversed garante que as ações serão realizadas do tweet mais recente ao mais antigo.
        last_seen_id_reply = mention.id
        if 'itabuna' in mention.full_text.lower() or 'itabocas' in mention.full_text.lower():
            try:
                api.create_favorite(mention.id)
            except tweepy.TweepError:
                print('DEU ERRO!')
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
        if ('itabuna' in search.text.lower() or 'itabocas' in search.text.lower())\
        and search.author.screen_name != 'itabuner':  # Se tem "itabuna" no tweet e ele não é do bot
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
