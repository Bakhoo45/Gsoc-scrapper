import pandas as pd

def csv(data):
    df = pd.DataFrame(data=data)
    df.to_csv("Projects.csv",index=False)
    print("The file has been cretead")


def excel(data):
    df = pd.DataFrame(data=data)
    writer = pd.ExcelWriter("Projects.xlsx", engine='xlsxwriter')
    df.to_excel(writer, index=False, sheet_name='GSoC Projects')
    

    worksheet = writer.sheets['GSoC Projects']
    for idx, col in enumerate(df.columns):

        max_length = max(
            df[col].astype(str).apply(len).max(), 
            len(str(col)) 
        ) + 2 
        worksheet.set_column(idx, idx, max_length)
    
    writer.close()
    print("Excel file has been created")

