from rivalz_client import RivalzClient
from dotenv import load_dotenv
from fpdf import FPDF
import os
import time

load_dotenv()

def create_sample_pdf():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    # Add some sample content
    pdf.cell(200, 10, txt="Sample PDF Document", ln=1, align='C')
    pdf.cell(200, 10, txt="", ln=1, align='L')
    pdf.multi_cell(0, 10, txt="This is a sample PDF document created for testing the Rivalz SDK. It contains some text that we can use to test the knowledge base and chat functionality. The document discusses artificial intelligence and its applications in modern technology.", align='L')
    pdf.multi_cell(0, 10, txt="AI has become an integral part of our daily lives, from virtual assistants to recommendation systems. Machine learning algorithms help process vast amounts of data to derive meaningful insights and make predictions.", align='L')
    
    # Save the PDF
    pdf.output("sample.pdf")
    return "sample.pdf"

def main():
    client = RivalzClient(os.getenv("RIVALZ_SECRET_TOKEN"))

    try:
        # Create a sample PDF file
        print("Creating sample PDF...")
        pdf_path = create_sample_pdf()
        
        # Upload the PDF file
        print("Uploading PDF file...")
        result = client.upload_file(pdf_path)
        print(f"File uploaded with IPFS hash: {result['ipfs_hash']}")

        # Create a knowledge base
        print("\nCreating knowledge base...")
        kb = client.create_knowledge_base("Test Knowledge Base", pdf_path)
        print(f"Knowledge base created with ID: {kb['id']}")

        # Wait for knowledge base to be ready
        print("\nWaiting for knowledge base to be ready...")
        while True:
            kb = client.get_knowledge_base(kb["id"])
            if kb["status"] == "ready":
                break
            time.sleep(1)
            print(".", end="", flush=True)

        # Chat with the knowledge base
        print("\n\nTesting chat...")
        response = client.chat(kb["id"], "What topics does this document discuss?")
        print(f"Chat response: {response['message']}")

    except Exception as e:
        print(f"\nError occurred: {e}")

if __name__ == "__main__":
    main() 