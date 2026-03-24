# steghide-mkv

**steghide-mkv** is a robust cybersecurity tool built on the foundation of steghide. It extends traditional steganography by allowing users to hide any file type within video containers using the **Rijndael-128 (AES)** encryption algorithm.

While it accepts a wide variety of input video formats, it is designed to specifically target and output the **Matroska (MKV)** format to ensure high data capacity and structural integrity.

---

## 🚀 Key Features

* **AES Encryption:** Utilizes **Rijndael-128** to ensure that your hidden data is encrypted before being embedded.  
* **Universal Input:** Accepts almost **any video format** as a source carrier.  
* **MKV Output:** Standardizes the output to `.mkv` to handle complex data embedding.  
* **High Capacity:** Supports embedding data that is **more than 2× the size** of the original source video file.  

---

## ⚠️ Important Considerations

* **File Expansion:** The output MKV files are often significantly larger than the original source. To keep file sizes manageable, it is recommended to use **smaller source videos**.

* **Data Fragility:**  
  > [!CAUTION]  
  > **Do not compress or re-encode** the output MKV file. Standard video compression (like uploading to some social media or using HandBrake) will likely **corrupt the hidden data**, making it unrecoverable.

---

## 📥 Installation & Setup

To get started with **steghide-mkv**, follow these steps to clone the repository and build the binary:

### 1. Clone the Repository

Open your terminal and run:

```bash
git clone https://github.com/Tarungopal15ea16/steghide-mkv.git
```
### 2. Enter the Directory 

```bash
cd steghide-mkv
```
### 3. Build the Tool

Compile the source code using the provided Makefile (requires administrative privileges):

```bash
sudo make
```
