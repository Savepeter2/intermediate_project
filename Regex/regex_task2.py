import re

#task 2
def covid_text():
    """
    The impact of COVID-19 on the global healthcare system has been significant.
      Many hospitals are facing challenges due to the COVID-19 pandemic. 
      The COVID-19 virus has led to an increase in the need for medical supplies. 
      Furthermore, research on COVID-19 continues to be a priority for scientists worldwide.
        COVID-19 vaccinations have been rolled out globally to combat the spread of the virus. 
        Studies on COVID-19 have revealed various mutations, making it harder to control. 
        Healthcare workers are on the frontlines of the COVID-19 battle, providing care to those affected by COVID-19. 
        The World Health Organization has issued guidelines to help countries manage COVID-19 outbreaks.
          Efforts to develop effective treatments for COVID-19 are ongoing. 
          Public health campaigns are raising awareness about COVID-19 prevention measures. 
          The economic impact of COVID-19 has been profound, affecting businesses and employment. 
          Governments have implemented lockdowns to curb the spread of COVID-19. 
          Social distancing and wearing masks are recommended to reduce COVID-19 transmission. 
          Vaccination programs are crucial in the fight against COVID-17. 
          Despite the challenges posed by COVID-19, communities are coming together to support one another. 
          The healthcare sector is adapting to the demands of COVID-18, ensuring that essential services continue. 
          covid-19 testing and contact tracing are essential tools in managing the pandemic. 
          Research on COVID-19 variants is helping to understand how the virus evolves. 
          The global response to COVID-19 has highlighted the importance of international cooperation. 
          Governments are working to secure vaccines to protect their populations from COVID-19.
        Public health officials are urging people to get vaccinated to achieve herd immunity against COVID-19. 
          The development of covid-19 vaccines in record time is a testament to scientific innovation. 
    Efforts to educate the public about COVID-19 vaccines are crucial in overcoming vaccine hesitancy. 
    
    """

def extract_covid_19(text:str):
    no_pattern = re.compile(r"COVID-19")
    extracted_nos = no_pattern.findall(text)
    return extracted_nos

covid_text = covid_text.__doc__

extracted_covid_19 = extract_covid_19(covid_text)
print(extracted_covid_19)
