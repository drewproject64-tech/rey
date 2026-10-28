"""Text formatting and extractive Spanish summarization helpers."""
import re
from collections import Counter

WORDS = re.compile(r"[A-Za-zÁÉÍÓÚÜÑáéíóúüñ]+")
STOP = {"para", "pero", "como", "porque", "sobre", "desde", "tiene", "tienen", "este", "esta", "estos", "estas", "también", "entre", "cuando", "donde", "las", "los", "por", "con", "una", "uno", "que", "del", "son", "más", "sus", "sin", "está", "fue", "ser", "una", "unos", "unas", "todo", "todos", "se", "de", "la", "el", "un", "lo", "y", "o", "al", "en", "es", "no", "su"}


def format_text(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r" *\n *", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r" +([,.;:!?])", r"\1", text)
    text = re.sub(r"([,;:!?])(?=[^\s\d\n])", r"\1 ", text)
    return text.strip()


def summarize_text(text: str) -> str | None:
    sentences = [
        s.strip() for s in re.split(r"(?<=[.!?])\s+|\n+", format_text(text))
        if s.strip()
    ]
    if len(sentences) < 3:
        return None
    tokenized = [[w.lower() for w in WORDS.findall(s)] for s in sentences]
    frequencies = Counter(
        w for words in tokenized for w in words if len(w) > 3 and w not in STOP
    )
    n = min(3, max(1, round(len(sentences) * 0.35)))
    if not frequencies:
        chosen = [0]
    else:
        scores = [
            sum(frequencies[w] for w in words) / max(len(words), 1) ** 0.5
            for words in tokenized
        ]
        chosen = sorted(sorted(range(len(sentences)), key=lambda i: -scores[i])[:n])
    return " ".join(sentences[i] for i in chosen)
