from misago.markdown.factory import *

# Monkeypatch blockquote parser to handle codes
from markdown import util
import markdown.blockprocessors
from markdown.extensions.fenced_code import FencedBlockPreprocessor

markdown.blockprocessors.BlockQuoteProcessor = FencedBlockPreprocessor