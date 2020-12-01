# Python Libraries
from datetime import datetime, timedelta
from fpdf import FPDF

# Local Imports
from simulations import networth, invested, yearly_cont, yearly_return, yearly_vol, final_median_val, withdraw, final_median_val

WIDTH = 210
HEIGHT = 297

def create_analytics_report(day='', filename="report.pdf"):
	pdf = FPDF() # A4 (210 by 297 mm)
	
	''' First Page '''
	pdf.add_page()
	pdf.image("./source/letterhead.png", 0, 0, WIDTH)
	create_title('11/28/2020', 'Investment Projections', pdf)

	pdf.set_font('Arial', '', 12)
	pdf.write(20, "Current Total Net Worth: ${:,}".format(round(networth)))
	pdf.ln(5)
	pdf.write(20, "Current Total Invested: ${:,}".format(round(invested)))
	pdf.ln(5)
	pdf.set_font('Arial', '', 9)
	pdf.write(20, "Assumptions:")
	pdf.ln(3.25)
	pdf.write(20, "Annual Contribution: ${:,}".format(round(yearly_cont,0)))
	pdf.ln(3.25)
	pdf.write(20, "Expected Yield: {:.1%}".format(yearly_return))
	pdf.ln(3.25)
	pdf.write(20, "Expected Volatility: {:.1%}".format(yearly_vol))

	pdf.image("./source/3quantiles.png", x = 42, y = 120, h = 0, w = 126)
	pdf.image("./source/allSimulations.png", x = 7, y = 215, h = 0, w = 95)
	pdf.image("./source/endingvalues.png", x = 115, y = 215, h = 0, w = 90)

	''' Second Page '''
	pdf.add_page()
	pdf.image("./source/letterhead.png", 0, 0, WIDTH)
	create_title('11/28/2020', 'Withdrawl Analysis', pdf)

	pdf.set_font('Arial', '', 12)
	pdf.write(20, "Retirement Starting Portfolio: ${:,}".format(round(final_median_val)))
	pdf.ln(5)
	pdf.write(20, "Yearly Withdrawl: ${:,}".format(round(withdraw)))
	pdf.ln(5)
	pdf.set_font('Arial', '', 9)
	pdf.write(20, "Assumptions:")
	pdf.ln(3.25)
	pdf.write(20, "Starting portfolio value from projection median")
	pdf.ln(3.25)
	pdf.write(20, "Expected Yield: {:.1%}".format(yearly_return))
	pdf.ln(3.25)
	pdf.write(20, "Expected Volatility: {:.1%}".format(yearly_vol))

	pdf.image("./source/3quantiles_with.png", x = 42, y = 120, h = 0, w = 126)
	pdf.image("./source/allSimulations_with.png", x = 7, y = 215, h = 0, w = 95)
	pdf.image("./source/endingvalues_with.png", x = 115, y = 215, h = 0, w = 90)
	
	pdf.output(filename, 'F')

def create_title(day, title, pdf):
	pdf.set_font('Arial', '', 24)  
	pdf.ln(60)
	pdf.write(5, f'{title}')
	pdf.ln(10)
	pdf.set_font('Arial', '', 16)
	pdf.write(4, f'{day}')
	pdf.ln(5)

if __name__ == '__main__':
	today = (datetime.today()).strftime("%m/%d/%y").replace("/0","/").lstrip("0")
	create_analytics_report(today)