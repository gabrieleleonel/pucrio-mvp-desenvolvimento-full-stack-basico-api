# Game Tracker API (Back-end)

Este é o back-end do projeto Game Tracker. A aplicação é uma API RESTful construída com Python e Flask, responsável por gerenciar um catálogo pessoal de jogos.

# Tecnologias Utilizadas

- Python 3
- Flask
- Flask-SQLAlchemy (ORM para o SQLite)
- Flask-CORS (Para permitir integração com o Front-end)
- Flasgger (Documentação Swagger)
- SQLite (Banco de Dados embutido)

# Pré-requisitos

Certifique-se de ter o Python (versão 3.8 ou superior) instalado em sua máquina.

# Instruções de Instalação e Execução

1. Clone o repositório ou baixe os arquivos
Coloque os arquivos app.py e requirements.txt em uma pasta no seu computador.

2. Crie e ative um ambiente virtual (Recomendado)
No terminal, dentro da pasta do projeto, execute:

## Windows
```shell
python -m venv venv
venv\Scripts\activate
```

## Linux/Mac
```shell
python3 -m venv venv
source venv/bin/activate
```

3. Instale as dependências

```shell
pip install -r requirements.txt
```

4. Execute a aplicação

```shell
python app.py
```

A API estará rodando em http://127.0.0.1:5000. O banco de dados games.db será criado automaticamente na primeira execução.

# Documentação da API (Swagger)

Para visualizar a documentação interativa da API, abra o navegador e acesse:
http://127.0.0.1:5000/apidocs ou a rota principal `/`, você será automaticamente redirecionado para a apidocs.

# Rotas Implementadas

- GET /games: Retorna a lista de todos os jogos.
- GET /games/<id>: Retorna os detalhes de um jogo específico.
- POST /games: Cadastra um novo jogo.
- PUT /games/<id>: Atualiza as informações de um jogo (ex: Status).
- DELETE /games/<id>: Remove um jogo do banco de dados.
