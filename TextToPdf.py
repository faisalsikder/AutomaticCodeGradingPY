########################################
# Faisal Sikder
# University of Miami
# Dept of Computer Science
########################################

from reportlab.pdfgen import canvas
from reportlab.lib.units import inch, cm
from reportlab.lib.pagesizes import letter, A4

def write_simple_pdf(directory,filename):
    comments = [line.strip() for line in open(directory+"\\"+filename+".txt")]
    #print submited_students
    pdf = canvas.Canvas(directory+"\\"+filename+".pdf",pagesize=letter)
    i=0;
    line_size  = 80
    for com in comments:
        while len(com)>= line_size:
            #print    len(com)
            last_space = com.find(" ",line_size)
            if last_space > 0:
                line = com[0:last_space]
            else:
                line = com
                last_space=len(com);
            pdf.drawString(30,740-i,line)
            com = com[last_space+1:]
            i+=15
        pdf.drawString(30,740-i,com)
        i+=22
    pdf.showPage()
    pdf.save()


#write_simple_pdf("G:\\Fall2016csc220\\Lab01\\csc220-aruh220", "aruh220_lab01_comments_t");