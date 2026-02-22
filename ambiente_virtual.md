# Criar o ambiente virtual:

- 1.conda create -n nome_ambiente python=3.10 -y
- 2.conda activate nome_ambiente
    - 2.1 pip install yt-dlp openai-whisper torch 
    - 2.2 winget install Gyan.FFmpeg ( obrigatório para Whisper — não é via pip)
    - 2.3 pip install pyinstaller


#### Para adicionar icone no programa e executar o programa simultaneamente:

> pyinstaller --noconfirm --onefile --windowed --icon "assets\app.ico" gui.py



