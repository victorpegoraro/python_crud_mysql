import PySimpleGUI as sg
import mysql.connector


def conectar():

  layoutbd = [ [sg.Text('Cenectar com banco de dados MySQL')],
            [sg.Text('Host ex :localhost', size=(20, 1)), sg.InputText(key='host')],
            [sg.Text('User ex: root', size=(20, 1)), sg.InputText(key='user')],
            [sg.Text('Senha ex: senha', size=(20, 1)), sg.InputText(key='pass')],
            [sg.Text('Database ex: crud_python', size=(20, 1)), sg.InputText(key='bd')],
            [sg.Text(size=(30,1), key='out')],
            [sg.Text(size=(15,1)),sg.Button('Conectar'), sg.Button("Sair")]]

  windowbd = sg.Window('CRUD Ptyhon - Conectar com BD', layoutbd)

  while True:             # Event Loop
    event, values = windowbd.read()
    print(event, values)
    if event in (None, 'Sair'):
        break
    if event == 'Conectar':
      try:
        mydb = mysql.connector.connect(
          host=values['host'],
          user=values['user'],
          passwd=values['pass'],
          database=values['bd']
        )

        mycursor = mydb.cursor()
        break

      except mysql.connector.errors.InterfaceError:
        notificacao = "Erro: Ative o banco de dados"
        windowbd['out'].update(notificacao)

      except mysql.connector.errors.DatabaseError:
        notificacao = "Erro: Não foi possivel conectar"
        windowbd['out'].update(notificacao)
  
  windowbd.close()
  if event == 'Conectar':
    login()



sg.theme('SandyBeach')  # Add some color to the window


#janela de login
def login():

  layout = [  [sg.Text('Login page')],
              [sg.Text('Usuario', size=(10, 1)), sg.InputText(key='usuario')],
              [sg.Text('Senha', size=(10, 1)), sg.InputText(key='senha')],
              [sg.Text(size=(30,1), key='out')],
              [sg.Text(size=(12,1)),sg.Button('Entrar'), sg.Button('Registrar'), sg.Button("Sair")]]

  window = sg.Window('CRUD Ptyhon - Login', layout)

  while True:             # Event Loop
    event, values = window.read()
    print(event, values)
    if event in (None, 'Sair'):
        break
    if event == 'Entrar':

      sql = "SELECT usuario FROM usuarios WHERE usuario = %s AND senha = %s "
      val = (values['usuario'], values['senha'])

      mycursor.execute(sql, val)

      conta = mycursor.fetchall()
      if len(conta) == 1:
        print(conta[0][0])
        break

      else:
        window['out'].update("Usuario ou senha incorreto")

    if event == "Registrar":
      break

  window.close()
  if event == "Entrar":
    user(conta[0][0])
  if event == "Registrar":
    registrar()


#Janela do usuario
def user(nome):

  layout1 = [ [sg.Text(f'Bem vindo {nome}')],
              [sg.Text(size=(30,1), key='out')],
              [sg.Button('Alterar dados'), sg.Button('Deletar conta'), sg.Button("Logout")]]

  window1 = sg.Window('CRUD Ptyhon - Conta', layout1)

  while True:  # Event Loop
    event, values = window1.read()
    print(event, values)
    if event in (None, 'Sair'):
        break

    if event == 'Deletar conta':

      sql = "DELETE FROM usuarios WHERE usuario = %s"
      val = (nome, )

      mycursor.execute(sql, val)

      mydb.commit()

      sg.popup('Conta deletada')
      break

    if event == "Alterar dados":
      break

    if event == 'Logout':
      break

  window1.close()
  if event == 'Deletar conta':
    login()
  if event == 'Alterar dados':
    alterar(nome)
  if event == 'Logout':
    login()


#Aterar dados
def alterar(nome):

  layout2 = [ [sg.Text(f'Alterar dados de {nome}')],
              [sg.Text('Usuario', size=(10, 1)), sg.InputText(key='user')],
              [sg.Text('Email', size=(10, 1)), sg.InputText(key='email')],
              [sg.Text('Senha', size=(10, 1)), sg.InputText(key='pass')],
              [sg.Text(size=(30,1), key='out')],
              [sg.Text(size=(15,1)),sg.Button('Alterar'), sg.Button("Voltar")]]

  window2 = sg.Window('CRUD Ptyhon - Alterar dados', layout2)

  while True:  # Event Loop
    event, values = window2.read()
    print(event, values)
    if event in (None, 'Voltar'):
        break

    if event == 'Alterar':

      if values['user'] and values['email'] and values['pass']:

        sql = "UPDATE usuarios SET usuario = %s, email = %s, senha = %s WHERE usuario = %s"
        val = (values['user'],values['email'],values['pass'],nome)

        mycursor.execute(sql, val)
        mydb.commit()
        window2['out'].update("Dados alterados")

      else:
        window2['out'].update("Preencha todos os campos")

  window2.close()
  if event in (None, 'Voltar'):
    user(nome)


#Registrar usuario
def registrar():

  layout3 = [[sg.Text('Cirar conta')],
            [sg.Text('Usuario', size=(10, 1)), sg.InputText(key='usuario')],
            [sg.Text('Email', size=(10, 1)), sg.InputText(key='email')],
            [sg.Text('Senha', size=(10, 1)), sg.InputText(key='senha')],
            [sg.Text(size=(30,1), key='out')],
            [sg.Text(size=(12,1)), sg.Button('Criar'), sg.Button("Voltar")]]

  window3 = sg.Window('CRUD Ptyhon - Criar conta', layout3)

  while True:  # Event Loop
    event, values = window3.read()
    print(event, values)
    if event in (None, None):
        break
    if event == 'Voltar':
        break

    if event == 'Criar':
      resposta  = criarusuario(values['usuario'], values['email'], values['senha'])
      window3['out'].update(resposta)

  window3.close()
  if event =='Voltar':
    login()


#Função para criar usuario
def criarusuario(usuario,email,senha):

  if usuario and email and senha:

    sql = "INSERT INTO usuarios (usuario, email, senha) VALUES (%s, %s, %s)"
    val = (usuario, email, senha)
    mycursor.execute(sql, val)
    mydb.commit()
    return "Conta criada"
  else:
    return "Preencha todos os campos"
    

if __name__ == "__main__":
    conectar()