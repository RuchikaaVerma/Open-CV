from PyPDF2 import PdfMerger
def merge_pdfs(pdf_list, output_path):
    merger = PdfMerger()
    for pdf in pdf_list:
        merger.append(pdf)
    merger.write(output_path)
    merger.close()
     
def main():
    print("Welcome to PDF Merger!")
    df_list=get_pdf_order()
    if validate_pdfs(pdf_list):
                output_path=input("Enter the output PDF file name (e.g., merged.pdf): ")
                merge_pdfs(pdf_list, output_path)
                print(f"PDFs merged successfully into '{output_path}'")  
            
    
        
# Example usage
#merge_pdfs(['book1.pdf', 'book2.pdf'], 'merged_output.pdf')
#print("PDFs merged successfully into 'merged_output.pdf'")
    
def get_pdf_order():
    pdf_list =input("Enter the PDF file names in desired order(comma-separated): ").split(',')
    return [pdf.strip() for pdf in pdf_list]

def validate_pdfs(pdf_list):
    for pdf in pdf_list:
        try:
            with open(pdf, 'rb') as f:
                pass
        except FileNotFoundError:
            print(f"File not found: {pdf}")
            return False
    return True 

pdf_order=get_pdf_order()
merge_pdfs(pdf_order, 'custom_merged_output.pdf')