import csv
import requests
from bs4 import BeautifulSoup


if __name__ == "__main__":

    majors_str = "anthropology, architecturalstudies, arthistory, astronomyastrophysics, biologicalchemistry, biologicalsciences, chemistry, cinemamediastudies, classicalstudies, cognitivescience, comparativehumandevelopment, comparativeliterature, caam, computationalsocialscience, computerscience, creativewriting, comparativeraceethnicstudies, datascience, democracystudies, digitalstudies, eastasianlanguagescivilizations, economics, educationandsociety, englishlanguageliterature, environmentalscience, environmentalstudies, cegu, fundamentalsissuesandtexts, genderstudies, geographicalstudies, geophysicalsciences, germanicstudies, globalstudies, healthandsociety, history, scienceandmedicinehips, humanrights, inequalityandsocialchange, Inquiryresearchhumanities, jewishstudies, latinamericanstudies, lawlettersandsociety, linguistics, mathematics, MediaArtsandDesign, medievalstudies, molecularengineering, music, neareasternlanguagescivilizations, neuroscience, norwegianstudies, philosophy, physics, politicalscience, psychology, publicpolicystudies, quantitativesocialanalysis, quantitativesocialanalysis, rdin, religiousstudies, renaissancestudies, romancelanguagesliteratures, slaviclanguagesliteratures, sciencecommunicationpublicdiscourse, sociology, southasianlanguagescivilizations, statistics, theaterperformancestudies, visualarts, yiddish"
    majors_list = majors_str.split(", ")


    with open('catalog.csv', mode='w', newline='', encoding='utf-8') as file:

        fieldnames = ['Department', 'Course Number', 'Description', 'Terms Offered', 'Equivalent Courses', 'Prerequisites', 'Instructors']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        
        writer.writeheader()
        
        for major in majors_list: # iterating through each major URL
            url = f'http://collegecatalog.uchicago.edu/thecollege/{major}/'

            response = requests.get(url) # http get request

            if response.status_code == 200: # successful?
                soup = BeautifulSoup(response.text, 'html.parser') # parsing with beautiful soup

                course_listings = soup.find_all(class_='courseblock') # finding course listings on page
            
                # Initialize variables for additional course information
                terms_offered = equivalent_courses = prerequisites = instructors = None

                for course_listing in course_listings:
                    # Extract department and course number
                    course_title = course_listing.find(class_='courseblocktitle').strong.text.strip()
                    department, course_number = course_title.split()[:2]
                    course_number = course_number.replace('.', '')

                    # description
                    description = course_listing.find(class_='courseblockdesc').text.strip()
                    other_info_element = course_listing.find(class_='courseblockdetail')
                    if other_info_element:
                        other_info = other_info_element.text.strip()

                        terms_offered = ''
                        equivalent_courses = ''
                        prerequisites = ''
                        instructors = ''

                        for line in other_info.split('\n'):
                            line = line.strip()
                            if line.startswith('Equivalent Course(s):'):
                                equivalent_courses = line.replace('Equivalent Course(s):', '').strip()
                            elif line.startswith('Prerequisite(s):'):
                                prerequisites = line.replace('Prerequisite(s):', '').strip()
                            elif line.startswith('Instructor(s):'):
                                info = line.split()
                                splitter_index = -1

                                for i,val in enumerate(info):
                                    if val == 'Terms':
                                        splitter_index = i
                                        break
                                
                                if splitter_index == -1:
                                    instructors = line.replace('Instructor(s):', '').strip()
                                else:
                                    instructors = " ".join(info[1:splitter_index]).strip()
                                    terms_offered = " ".join(info[splitter_index+2:]).strip()
                                
                                
                        var_list = [terms_offered, equivalent_courses, prerequisites, instructors]
                        for i,val in enumerate(var_list):
                            if val == '':
                                var_list[i] = 'Unspecified'
                        terms_offered, equivalent_courses, prerequisites, instructors = var_list
                                

                        writer.writerow({'Department': department, 'Course Number': course_number, 'Description': description, 'Terms Offered': terms_offered, 'Equivalent Courses': equivalent_courses, 'Prerequisites': prerequisites, 'Instructors': instructors})
                
            else:
                print(f"Failed to retrieve the webpage for {major}. Status code:", response.status_code)