from .nodes.RBG_lora_key_converter_node import (
    RBGLoraKeyConverterNode,
)

NODE_CLASS_MAPPINGS = {
    "RBGLoraKeyConverterNode": RBGLoraKeyConverterNode,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "RBGLoraKeyConverterNode": "RBG LoRA Key Converter 🔑",
}

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]
