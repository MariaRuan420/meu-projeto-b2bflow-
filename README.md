# Desafio Técnico - Integração Supabase + Z-API (Python)

Este repositório contém a solução do desafio prático de automação para leitura de contatos e envio de mensagens customizadas via WhatsApp.

## 🚀 Setup da Tabela no Supabase

Crie uma tabela chamada `contatos` no seu projeto do Supabase utilizando o comando SQL abaixo no editor do painel:

```sql
create table contatos (
  id bigint generated always as identity primary key,
  nome text not null,
  telefone text not null,
  created_at timestamp with time zone default timezone('utc'::text, now()) not null
);

-- Inserção de dados de teste (insira até 3 números válidos com DDD)
insert into contatos (nome, telefone) values 
('Fulano', '27999998888'),
('Ciclano', '27988887777');
```

## ⚙️ Configuração do Ambiente

1. Clone o repositório para sua máquina local.
2. Crie um arquivo na raiz do projeto chamado `.env`.
3. Preencha o `.env` seguindo o modelo abaixo com as suas credenciais gratuitas:

```ini
SUPABASE_URL=https://supabase.co
SUPABASE_KEY=sua-chave-anon-public-do-supabase
ZAPI_INSTANCE_ID=SUA_INSTANCIA_AQUI
ZAPI_TOKEN=SEU_TOKEN_AQUI
ZAPI_CLIENT_TOKEN=SEU_CLIENT_TOKEN_OPCIONAL
```

## 🛠️ Como Executar o Projeto

Instale as dependências necessárias e execute o script principal:

```bash
# Instalar as bibliotecas
pip install -r requirements.txt

# Executar a automação
python main.py
```