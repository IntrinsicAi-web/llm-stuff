import re
from typing import Dict, Iterable, List, Mapping, Optional, Union


class SimpleTokenizerV1:
    def __init__(
        self,
        vocab: Union[Mapping[str, int], Iterable[str]],
        *,
        unknown_token: Optional[str] = "<unk>",
        auto_add_new_tokens: bool = False,
    ):
        if isinstance(vocab, Mapping):
            self.str_to_int: Dict[str, int] = dict(vocab)
        else:
            self.str_to_int = {token: idx for idx, token in enumerate(vocab)}

        self.unknown_token = unknown_token
        self.auto_add_new_tokens = auto_add_new_tokens

        if self.unknown_token is not None:
            self.unknown_token_id = self.str_to_int.setdefault(
                self.unknown_token, len(self.str_to_int)
            )
        else:
            self.unknown_token_id = None

        self.int_to_str = {index: token for token, index in self.str_to_int.items()}

    def encode(self, text: str) -> List[int]:
        preprocessed = re.split(r'([,.:;?_!"()\']|--|\s)', text)
        tokens = [item.strip() for item in preprocessed if item.strip()]
        ids: List[int] = []
        for token in tokens:
            token_id = self.str_to_int.get(token)
            if token_id is None:
                if self.auto_add_new_tokens:
                    token_id = len(self.str_to_int)
                    self.str_to_int[token] = token_id
                    self.int_to_str[token_id] = token
                elif self.unknown_token_id is not None:
                    token_id = self.unknown_token_id
                else:
                    raise ValueError(
                        f"Token {token!r} is not in the vocabulary and no "
                        "unknown token handling is configured"
                    ) from None
            ids.append(token_id)
        return ids

    def decode(self, ids: Iterable[int]) -> str:
        tokens: List[str] = []
        for idx in ids:
            token = self.int_to_str.get(idx)
            if token is None:
                if self.unknown_token is not None:
                    token = self.unknown_token
                else:
                    raise ValueError(
                        f"Token id {idx} is not in the vocabulary and no "
                        "unknown token handling is configured"
                    ) from None
            tokens.append(token)
        text = " ".join(tokens)
        return re.sub(r"\s+([,.:;?_!\"()'])", r"\1", text)