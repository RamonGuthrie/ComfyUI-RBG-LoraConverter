import torch
import os
import glob
import time
from safetensors.torch import load_file, save_file
import folder_paths
from tqdm import tqdm

class RBGLoraKeyConverterNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "input_path": ("STRING", {
                    "default": "path/to/your/lora.safetensors or /path/to/lora_folder",
                    "tooltip": "Path to a single .safetensors file or a directory containing .safetensors files."
                }),
                "output_dir": ("STRING", {
                    "default": folder_paths.get_output_directory(),
                    "tooltip": "Directory where the converted files will be saved."
                }),
                "output_filename_prefix": ("STRING", {
                    "default": "converted",
                    "tooltip": "Prefix to be added to the output filenames."
                }),
                "dry_run": ("BOOLEAN", {
                    "default": False,
                    "tooltip": "If enabled, the conversion will be simulated without saving any files."
                }),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("summary",)
    FUNCTION = "convert_lora_hub"
    CATEGORY = "RBG/RBGLoraKeyConverter"

    def convert_lora_hub(self, input_path, output_dir, output_filename_prefix, dry_run):
        start_time = time.time()
        if not os.path.exists(input_path):
            return (f"Error: Input path does not exist: {input_path}",)

        files_to_convert = []
        if os.path.isfile(input_path):
            if input_path.endswith('.safetensors'):
                files_to_convert.append(input_path)
            else:
                return (f"Error: Selected file is not a .safetensors file.",)
        elif os.path.isdir(input_path):
            files_to_convert = glob.glob(os.path.join(input_path, '*.safetensors'))
            if not files_to_convert:
                return (f"Error: No .safetensors files found in the selected directory.",)

        if not dry_run and not os.path.exists(output_dir):
            os.makedirs(output_dir)

        processed_count = len(files_to_convert)
        converted_count = 0
        skipped_count = 0
        error_count = 0
        
        pbar = tqdm(total=processed_count, desc="Converting LoRAs")

        for file_path in files_to_convert:
            try:
                base_name = os.path.basename(file_path)
                name, ext = os.path.splitext(base_name)
                output_filename = f"{name}_{output_filename_prefix}{ext}"
                output_path = os.path.join(output_dir, output_filename)

                if os.path.exists(output_path):
                    print(f"Skipping conversion for {base_name} as it already exists in the output directory.")
                    skipped_count += 1
                    pbar.update(1)
                    continue
                
                if dry_run:
                    print(f"[Dry Run] Would convert {base_name} to {output_path}")
                    converted_count += 1
                else:
                    self.process_conversion(file_path, output_path)
                    converted_count += 1

            except Exception as e:
                print(f"Failed to convert {os.path.basename(file_path)}: {e}")
                error_count += 1
            finally:
                pbar.update(1)
        
        pbar.close()
        
        end_time = time.time()
        elapsed_time = end_time - start_time
        
        summary = (
            f"Conversion {'(Dry Run)' if dry_run else 'complete'} in {elapsed_time:.2f} seconds. "
            f"Output directory: {output_dir}. "
            f"Processed: {processed_count}. "
            f"Converted: {converted_count}. "
            f"Skipped: {skipped_count}. "
            f"Errors: {error_count}."
        )
        
        print(summary)
        return (summary,)

    def process_conversion(self, input_path, output_path):
        try:
            state_dict = load_file(input_path)
            new_state_dict = {}
            sds_sd = state_dict.copy()

            final_layer_keys_forward = {
                "lora_unet_final_layer_adaLN_modulation_1.lora_down.weight": "norm_out.linear.lora_A.weight",
                "lora_unet_final_layer_adaLN_modulation_1.lora_up.weight": "norm_out.linear.lora_B.weight",
                "lora_unet_final_layer_linear.lora_down.weight": "proj_out.lora_A.weight",
                "lora_unet_final_layer_linear.lora_up.weight": "proj_out.lora_B.weight",
            }
            final_layer_keys_reverse = {v: k for k, v in final_layer_keys_forward.items()}

            is_forward = any(k in sds_sd for k in final_layer_keys_forward)
            is_reverse = any(k in sds_sd for k in final_layer_keys_reverse)

            conversion_performed = False
            if is_forward:
                print(f"Performing forward conversion for {os.path.basename(input_path)}")
                for old_key, new_key in final_layer_keys_forward.items():
                    if old_key in sds_sd:
                        value = sds_sd.pop(old_key)
                        if "adaLN_modulation" in old_key:
                            shift, scale = value.chunk(2, dim=0)
                            value = torch.cat([scale, shift], dim=0)
                        new_state_dict[new_key] = value
                conversion_performed = True
            elif is_reverse:
                print(f"Performing reverse conversion for {os.path.basename(input_path)}")
                for old_key, new_key in final_layer_keys_reverse.items():
                    if old_key in sds_sd:
                        value = sds_sd.pop(old_key)
                        if "adaLN_modulation" in new_key:
                            scale, shift = value.chunk(2, dim=0)
                            value = torch.cat([shift, scale], dim=0)
                        new_state_dict[new_key] = value
                conversion_performed = True

            if not conversion_performed:
                print(f"No convertible keys found in {os.path.basename(input_path)}. Saving as is.")

            for key, value in sds_sd.items():
                new_state_dict[key] = value

            save_file(new_state_dict, output_path)
            print(f"Successfully converted and saved to: {output_path}")
        except Exception as e:
            raise RuntimeError(f"Error processing {input_path}: {e}")

NODE_CLASS_MAPPINGS = {
    "RBGLoraKeyConverterNode": RBGLoraKeyConverterNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "RBGLoraKeyConverterNode": "RBG LoRA Key Converter 🔑"
}
