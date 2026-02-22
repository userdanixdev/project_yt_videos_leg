# 🎬 VideoTraduzido

![Python](https://img.shields.io/badge/Python-3.10-blue)
![Whisper](https://img.shields.io/badge/OpenAI-Whisper-green)
![PyInstaller](https://img.shields.io/badge/Packaging-PyInstaller-orange)
[![Conda](https://img.shields.io/badge/Conda-Environment-44A833?logo=anaconda&logoColor=white)](https://docs.conda.io/)
![License](https://img.shields.io/badge/License-Educational-lightgrey)
![Platform](https://img.shields.io/badge/Platform-Windows-blue)

### Objetivo do Projeto:

Atualmente, grande parte das aulas e conteúdos educacionais disponíveis online, especialmente nas áreas de tecnologia e programação que são produzidos em inglês e muitas vezes não possuem legendas em português. Isso pode dificultar o aprendizado para estudantes que não dominam totalmente o idioma.

A Aplicação Desktop desenvolvida em Python com o objetivo de:

- Baixar aulas do YouTube
- Transcrever áudio com IA (Whisper)
- Traduzir automaticamente para Português
- Gerar legenda `.srt`
- Organizar arquivos automaticamente

*A proposta é facilitar o acesso ao conhecimento, permitindo que usuários assistam a aulas em inglês com suporte de legendas traduzidas automaticamente, tornando o aprendizado mais acessível e inclusivo.*

---

### 🏗 Arquitetura do Sistema

```
YouTube URL
    ↓
yt-dlp
    ↓
FFmpeg
    ↓
Whisper (ASR + timestamps)
    ↓
Google Translator (EN → PT)
    ↓
SRT Generator
    ↓
Desktop/video_traduzido/
```

### 📁 Estrutura do Projeto

```
project_yt_videos_leg
|
├── yt_leg/
|      └── assets/
|      └── build/
|      └── dist/
|            └── VideoTraduzido.exe
|      └── gui.py
|      └── gui.spec
├── .gitignore
├── ambiente_virtual.md
├── README.md
├── requeriments.txt
```

**Output gerado automaticamente:**
```
Desktop/
└── video_traduzido/
    └── Nome_da_Aula/
        ├── Aula.mp4
        └── Aula.srt
```

### ⚙️ Stack Tecnológica


| Ferramenta | Função |
|------------|--------|
| Python 3.10 | Linguagem principal |
| Tkinter | Interface gráfica |
| yt-dlp | Download do YouTube |
| FFmpeg | Manipulação de áudio |
| Whisper (OpenAI) | Transcrição com timestamps |
| deep-translator | Tradução EN → PT |
| PyInstaller | Geração do executável |

---

### 🚀 Como Executar o Projeto

## 1️⃣ Criar ambiente

```
conda create -n yt_sub python=3.10
conda activate yt_sub

Instalar dependências
pip install yt-dlp openai-whisper torch deep-translator pyinstaller

Instalar FFmpeg (Windows)
winget install Gyan.FFmpeg

Instalar FFmpeg (Windows)
winget install Gyan.FFmpeg
```

#### ▶ Executar versão Python
> python gui.py

#### 📦 Gerar Executável (.exe)
> pyinstaller gui.spec

#### 📊 Performance

|Duração do Vídeo|	Modelo|	Tempo Médio (CPU)|
|------------|--------|------|
|10 min| small|	3–6 min|
|30 min|	small	|10–20 min|
|1 hora|	small	|25–50 min|

### 🧪 Problemas Encontrados e Soluções

> Erro: mel_filters.npz not found

**PyInstaller não incluía arquivos internos do Whisper.**
```

**Solução:**
- Criado gui.spec incluindo:
    > datas=[(whisper_assets, 'whisper/assets')]
```

**Erro 401 HuggingFace**
```
Causa:
Tentativa de usar modelo HuggingFace exigindo autenticação.

Solução:
Remoção completa do Transformers.
Substituído por deep-translator (Google Translate).
```

**Legenda não aparecia no VLC**

Causa:
> Arquivo salvo como _pt.srt.

Solução:
> Salvar como mesmo nome do vídeo:

**BASE_DIR NOT FOUND**

**Causa:**
> Diretório não era criado corretamente no .exe.

**Solução:**

> BASE_DIR.mkdir(parents=True, exist_ok=True)

### ⏳ Performance

**Teste real:**
- Aula: 30 minutos
- Modelo: Whisper small
- CPU (sem GPU)
- ⏱ Tempo médio: 10–20 minutos

### Pontos Fortes:

- 100% local (sem API paga)
- Organização automática
- Interface gráfica simples
- Executável portátil
- Tradução automática
- Estrutura escalável

### 🛡 Boas Práticas Aplicadas

- Organização automática de arquivos
- Threading para evitar travamento da UI
- Empacotamento controlado via .spec
- Separação de responsabilidades
- Tratamento de exceções estruturado
- Diretórios criados dinamicamente


### Considerações Legais

O download deve respeitar:

- Direitos autorais
- Termos de uso do YouTube
- Uso educacional ou autorizado

👨‍💻 Autor:

**Daniel Martins França**  

## 📬 Contato:

- 📧 Email: [f.daniel.m@gmail.com](mailto:f.daniel.m@gmail.com)  
- 💼 LinkedIn: [www.linkedin.com/in/danixdev](https://www.linkedin.com/in/danixdev)  

*Projeto desenvolvido para fins educacionais e estudo de processamento de áudio, IA aplicada, empacotamento de aplicações e engenharia de software desktop*
