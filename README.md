# ComfyUI-RBG-LoRA-Converter 🔑

[![ComfyUI Compatible](https://img.shields.io/badge/ComfyUI-Compatible-blue?style=for-the-badge)](https://github.com/comfyanonymous/ComfyUI)
[![1 Node](https://img.shields.io/badge/Nodes-1-green?style=for-the-badge)](https://github.com/RamonGuthrie/ComfyUI-RBG-LoraConverter)
[![1 Category](https://img.shields.io/badge/Categories-1-orange?style=for-the-badge)](https://github.com/RamonGuthrie/ComfyUI-RBG-LoraConverter)

<img width="1841" height="1054" alt="Screenshot 2025-07-22 174215" src="https://github.com/user-attachments/assets/4394f507-f060-4c97-ae10-609030c0a22e" />

A simple but powerful LoRA key converter for ComfyUI. This node is designed to help you convert LoRA models with old or non-standard key names to the new format, ensuring compatibility with the latest versions of ComfyUI and other platforms.

📝 This node also fixes issues with LoRA models trained and produced with [FAL.AI](https://fal.ai), which may not work correctly in [ComfyUI](https://github.com/comfyanonymous/ComfyUI) or with [ComfyUI-nunchaku](https://github.com/nunchaku-tech/ComfyUI-nunchaku) nodes.

***

## Troubleshooting

If you are having issues with LoRA models trained with [FAL.AI](https://fal.ai), this node can help. These models often have non-standard key names that can cause them to fail in ComfyUI. This node will automatically convert the keys to the correct format, allowing you to use them in your workflows.

## Feature List 🚀

*   **Batch Conversion:** Convert a single LoRA file or an entire directory of LoRA files at once.
*   **Dry Run Mode:** Simulate the conversion process without actually modifying any files, allowing you to see what changes will be made.
*   **Customizable Output:** Specify a custom output directory and filename prefix for your converted files.
*   **Error Handling:** The node will skip files that have already been converted and report any errors that occur during the conversion process.

***

## Installation 🛠️

1.  Clone this repository into your `ComfyUI/custom_nodes` directory:
    ```
    git clone https://github.com/RamonGuthrie/ComfyUI-RBG-LoraConverter.git
    ```
2.  Install the required dependencies by running the following command in your terminal:
    ```
    pip install -r requirements.txt
    ```
3.  Restart ComfyUI.

***

## Usage 🚀

After installation, you can find the `RBG LoRA Key Converter` node under the `RBG/RBGLoraKeyConverter` category in ComfyUI.

***

## Contributing ❤️

Contributions are always welcome! If you have any suggestions, improvements, or new ideas, please feel free to submit a pull request or open an issue.

***

## License 📜

This project is licensed under the MIT License.
