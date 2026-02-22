# Criar o ambiente virtual:

- 1.conda create -n nome_ambiente python=3.10 -y
- 2.conda activate nome_ambiente
    - 2.1 pip install yt-dlp openai-whisper torch 
    - 2.2 winget install Gyan.FFmpeg ( obrigatório para Whisper — não é via pip)
    - 2.3 pip install pyinstaller


#### Para adicionar icone no programa e executar o programa simultaneamente:

> pyinstaller --noconfirm --onefile --windowed --icon "assets\app.ico" gui.py


### Versionamento no ambiente virtual:

**GitHub CLI (gh), resolve autenticação sem precisar mexer manualmente com SSH.**

> GitHub.com

```
O GitHub CLI cria um token com permissões básicas (repo, workflow etc).
Excluir repositório é uma permissão separada, chamada delete_repo, e não vem por padrão (por segurança).
```
> gh auth login
- Se autenticar por gh, o token não tem permissão para deletar repositórios via gh.

```
Usando gh, não precisa de SSH ( se quiser )
Pode usar HTTPS + token automaticamente, o que evita dor de cabeça com chave pública.
```
#### Para deleção de repositórios:

> gh auth refresh -h github.com -s delete_repo

Autorize adicção de permissão **'delete_repo'** ao seu token atual.

> gh repo delete userdanixdev/project_yt_videos_leg --yes

**Logo pode usar novamente:**

>gh repo create project_yt_videos_leg --source=. --public --push





