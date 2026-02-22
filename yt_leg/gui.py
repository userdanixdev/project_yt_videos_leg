import os
import re
import threading
import subprocess
from pathlib import Path
import tkinter as tk
from tkinter import messagebox

import whisper
from deep_translator import GoogleTranslator


# ============================
# Config
# ============================

WHISPER_MODEL_NAME = "small"  # tiny/base/small/medium/large

def get_desktop_dir() -> Path:
    userprofile = os.environ.get("USERPROFILE")
    if userprofile:
        desktop = Path(userprofile) / "Desktop"
        if desktop.exists():
            return desktop
    return Path.home()

DESKTOP_DIR = get_desktop_dir()
BASE_DIR = DESKTOP_DIR / "video_traduzido"
BASE_DIR.mkdir(parents=True, exist_ok=True)

_whisper_model = None
_translator = None


# ============================
# Helpers
# ============================

def run(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True)

def sanitize_filename(name: str) -> str:
    name = re.sub(r"[\\/:*?\"<>|]+", "_", name)
    name = re.sub(r"\s+", " ", name).strip()
    return name[:140] if len(name) > 140 else name

def format_time(seconds: float) -> str:
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    ms = int((seconds - int(seconds)) * 1000)
    return f"{h:02}:{m:02}:{s:02},{ms:03}"

def chunk_text(text: str, max_chars: int = 420) -> list[str]:
    text = (text or "").strip()
    if not text:
        return []
    if len(text) <= max_chars:
        return [text]
    chunks, cur, cur_len = [], [], 0
    for w in text.split():
        add = len(w) + (1 if cur else 0)
        if cur_len + add > max_chars:
            chunks.append(" ".join(cur))
            cur, cur_len = [w], len(w)
        else:
            cur.append(w)
            cur_len += add
    if cur:
        chunks.append(" ".join(cur))
    return chunks


# ============================
# Models
# ============================

def ensure_models(status_label: tk.Label) -> None:
    global _whisper_model, _translator
    if _whisper_model is None:
        status_label.config(text="Carregando Whisper...")
        _whisper_model = whisper.load_model(WHISPER_MODEL_NAME)
    if _translator is None:
        # GoogleTranslator usa web. Não precisa token.
        status_label.config(text="Preparando tradutor EN→PT...")
        _translator = GoogleTranslator(source="en", target="pt")


# ============================
# Pipeline
# ============================

def download_youtube(url: str, status_label: tk.Label) -> Path:
    status_label.config(text="Baixando vídeo (yt-dlp)...")

    # baixa na BASE_DIR e depois move pra subpasta
    outtmpl = str(BASE_DIR / "%(title).140s [%(id)s].%(ext)s")
    run([
        "yt-dlp",
        "-f", "bv*+ba/best",
        "--merge-output-format", "mp4",
        "-o", outtmpl,
        url
    ])

    videos = sorted(BASE_DIR.glob("*.mp4"), key=lambda p: p.stat().st_mtime, reverse=True)
    if not videos:
        raise RuntimeError("Download terminou, mas não encontrei .mp4 em 'video_traduzido'.")

    video_path = videos[0]

    folder_name = sanitize_filename(video_path.stem)
    aula_folder = BASE_DIR / folder_name
    aula_folder.mkdir(parents=True, exist_ok=True)

    new_video_path = aula_folder / video_path.name
    if new_video_path.exists():
        new_video_path = aula_folder / f"{video_path.stem}_novo{video_path.suffix}"

    video_path.rename(new_video_path)
    return new_video_path


def transcribe_and_translate_to_srt(video_path: Path, status_label: tk.Label) -> Path:
    ensure_models(status_label)

    status_label.config(text="Transcrevendo áudio (EN) com Whisper...")
    result = _whisper_model.transcribe(str(video_path), language="en", task="transcribe")
    segments = result.get("segments", [])
    if not segments:
        raise RuntimeError("Whisper não retornou segmentos. Verifique se o vídeo tem áudio audível.")

    # mesmo nome do vídeo => VLC carrega automático
    srt_path = video_path.with_suffix(".srt")

    status_label.config(text="Traduzindo para PT e gerando SRT...")
    with open(srt_path, "w", encoding="utf-8") as f:
        idx = 1
        for seg in segments:
            text_en = (seg.get("text") or "").strip()
            if not text_en:
                continue

            start = format_time(seg["start"])
            end = format_time(seg["end"])

            parts = chunk_text(text_en)
            translated_parts = []
            for part in parts:
                # Tradução via Google (web)
                translated_parts.append(_translator.translate(part).strip())

            text_pt = " ".join(translated_parts).strip()

            f.write(f"{idx}\n")
            f.write(f"{start} --> {end}\n")
            f.write(f"{text_pt}\n\n")
            idx += 1

    return srt_path


def process(url: str, status_label: tk.Label):
    try:
        video_path = download_youtube(url, status_label)
        srt_path = transcribe_and_translate_to_srt(video_path, status_label)

        status_label.config(text="✅ Concluído!")
        messagebox.showinfo(
            "Sucesso",
            "Finalizado!\n\n"
            f"Vídeo: {video_path}\n"
            f"Legenda: {srt_path}\n\n"
            "Abra o MP4 no VLC. A legenda deve carregar automaticamente.\n"
            "Se não carregar: VLC > Legenda > Adicionar arquivo..."
        )
    except subprocess.CalledProcessError as e:
        status_label.config(text="Erro.")
        messagebox.showerror("Erro", f"Falha ao executar comando externo.\n\n{e}")
    except Exception as e:
        status_label.config(text="Erro.")
        messagebox.showerror("Erro", str(e))


def iniciar_processo():
    url = entry.get().strip()
    if not url:
        messagebox.showwarning("Aviso", "Cole o link do YouTube.")
        return

    status_label.config(text="Iniciando...")
    threading.Thread(target=process, args=(url, status_label), daemon=True).start()


# ============================
# UI
# ============================

root = tk.Tk()
root.title("YouTube → Legenda em Português (Local)")
root.geometry("640x250")

tk.Label(root, text="Cole o link do YouTube:").pack(pady=10)

entry = tk.Entry(root, width=92)
entry.pack()

tk.Button(root, text="Baixar e Gerar Legenda (PT)", command=iniciar_processo).pack(pady=12)

status_label = tk.Label(root, text="", wraplength=610)
status_label.pack(pady=8)

tk.Label(root, text=f"Saída: {BASE_DIR}").pack(pady=2)

root.mainloop()
