import qrcode
import pandas as pd
from PIL import Image
import os
import hashlib,json
# --- CSV path ---
path = r'/mnt/c/Users/johns/Downloads/finalemployeelist.csv'
df = pd.read_csv(path)

# --- Template path ---
template_path = "ecomiaa.png"

# --- Output folder ---
output_dir = "./output_qr"
os.makedirs(output_dir, exist_ok=True)

# --- Settings ---
qr_size = 400           # QR size
bg_margin = 100         # margin around QR
secret_numbers = []
for index, i in df.iterrows():
    # Step 1: Generate QR Data
    emp_no_str = str(i['EmpNo'])
    hash_id=hashlib.sha256(emp_no_str.encode())
    hash_id_digest = hash_id.hexdigest()
    secret_numbers.append(hash_id_digest)
    info = {
        "name": i['EmpName'],
        "idNumber":int(i["EmpNo"]),
        "secretNumber": hash_id_digest,

    }

    json_info = json.dumps(info)

    # Step 2: Create QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(json_info)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white").convert('RGBA')

    # Step 3: Resize QR
    qr_img = qr_img.resize((qr_size, qr_size), Image.LANCZOS)

    # Step 4: Load background template
    background = Image.open(template_path).convert('RGBA')

    # Step 5: Resize background to be bigger than QR
    bg_width = qr_size + bg_margin * 4
    bg_height = qr_size + bg_margin * 4
    background = background.resize((bg_width, bg_height), Image.LANCZOS)

    # Step 6: Center QR on background
    pos = ((bg_width - qr_size) // 2 - 15, (bg_height - qr_size) // 2)``
    background.paste(qr_img, pos, qr_img)

    # Step 7: Save output
    output_path = os.path.join(output_dir, f"{i['EmpName']}_qr.png")
    background.save(output_path)
    print(f"✅ Saved: {output_path}")

df["secretNumber"] = secret_numbers

    # --- Save updated CSV ---
updated_csv_path = os.path.join(output_dir, "finalemployeelist_with_secret.csv")
df.to_csv(updated_csv_path, index=False, encoding="utf-8-sig")


