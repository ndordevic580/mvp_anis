# Importing the required modules
import re
from PyPDF2 import PdfReader # pip install PyPDF2
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS # pip install wordcloud
from collections import Counter
stop_words = set(stopwords.words('english'))
import fitz
import io
from PIL import Image


class PDFCV:
    """
    A class used to read a PDF file and extract the content

    ...

    Attributes
    ----------
    path : str
        path pointing to the PDF file location 

    Methods
    -------
    read_pdf()
        Returns PdfReader object instance used to read the PDF file
    get_pdf_metadata()
        Returns a dictionary which stores document metadata
    pdf_to_text()
        Returns text data collected (appended) after iterating through pages
    clean_text(text)
        Returns cleaned text, mostly added spaces between merged words
    extract_features(text)
        Returns a dictionary which stores basic features
    normalize_text(text)
        Returns normalized text after removing punctuations, spaces, digits, etc.
    k_most_freq_words(text, freq_count)
        Returns a Counter object instance which outputs most frequnet words based on user selection
    create_wordcloud(text)
        Plots a word cloud based on extracted text
    extract_image()
        Downloads images found in the PDF file
    skill_extractor(skill_list, dict_key, tokens, skill_dict)
        Helper method for looping through mapped features in the corpus   
    extract_tech_features(normalized_text)
        Returns a dictionary of tech tools found in the document
    score(skill_dict)
        Returns a float and integer based score, first is the relevant one based on the role
    """
    def __init__(self, path):
        """Constructor method
        
        Parameters
        ----------
        path : str
            Document location path
        """
        self.path = path
    
    
    def read_pdf(self):
        """Loads the document path into a PdfReader object

        Returns
        ------
        PdfReader object
        """
        # Read PDF object and returning as text
        return PdfReader(self.path, 'rb')
    
    
    def get_pdf_metadata(self):
        """Creates document metadata dictionary

        Returns
        ------
        Dict with document metadata
        """
        # Read PDF object and collecting the metadata
        meta = self.read_pdf().metadata
        # Populate the metadata dict
        meta_dict = {
          "author": meta.author,
          "creator": meta.creator,
          "producer": meta.producer,
          "subject": meta.subject,
          "title": meta.title
        }
        return meta_dict
    
    
    def pdf_to_text(self):
        """Reads the document and extracts text

        Returns
        ------
        String containing fetched text
        """
        text = ""
        for page in self.read_pdf().pages:
            text += page.extract_text()
        return text
    
    
    def clean_text(self, text):
        """Cleans the text by unmerging words that were merged during the document read

        Parameters
        ----------
        text : str
            The raw extracted text

        Returns
        ------
        String containing cleaned text
        """
        new_text = re.sub("BORČAKDATA",'BORČAK DATA', text)
        new_text = re.sub("ANALYSTSarajevo",'ANALYST Sarajevo', new_text)
        new_text = re.sub("Iamadataengineer/dataanalystwith6yearsofhands-onexperienceinthebigdataindustry.Myjobinvolvedthecompletelifecycleofdataanalysiswhichincludedcollectingrawdatafromdiﬀerentinputs,performingawidespectrumofcalculations,andprovidingresultsorsuggestionsforfutureuse.Dataengineeringisacorepartofmyexperience,notonlyincreatinganalyticalmodelsandengines,butalsoputtingthemtouseinproduction.Itendtocreateandanalyzedataﬂowsandalgorithmswiththetechnicalarchitectureofthepipelineinmind,whichimprovesfurthersolutionsthatcanlaterbeutilizedfordeeperunderstandingandevaluationofthe data itself.Iamawell-organizedandcommittedengineer.Mypreviouseducationandexperiencehelpmetounderstandand solve complex problems in algorithmic design and data managing ﬂows.",
                          " I am a data engineer / data analyst with 6 years of hands-on experience in the big data industry. My job involved the complete life cycle of data analysis which included collecting raw data from diﬀerent inputs, performing a wide spectrum of calculations, and providing results or suggestions for future use. Data engineering is a core part of my experience, not only in creating analytical models and engines, but also putting them to use in production. I tend to create and analyze data ﬂows and algorithms with the technical architecture of the pipeline in mind, which improves further solutions that can later be utilized for deeper understanding and evaluation of the data itself. I am a well-organized and committed engineer. My previous education and experience help me to understand and solve complex problems in algorithmic design and data managing ﬂows.",
                          new_text)
        new_text = re.sub("FORMAL EDUCATIONBachelor’sdegree,Computerscience,SarajevoSchoolofScienceandTechnology–BuckinghamUniversity-Thesis topic: Sorting with fragile elements",
                          "FORMAL EDUCATION Bachelors degree, Computer science, Sarajevo School of Science and Technology–Buckingham University-Thesis topic: Sorting with fragile elements",
                          new_text)
        new_text = re.sub("CURRENT RESPONSIBILITIES●Data preprocessing●Data analysis●Report writing●Research and development of POC projects●Interviewing",
                          " CURRENT RESPONSIBILITIES●Data preprocessing●Data analysis●Report writing●Research and development of POC projects●Interviewing ",
                          new_text)
        new_text = re.sub("PROJECTSDATA ENGINEERING",
                          "PROJECTS DATA ENGINEERING",
                          new_text)
        new_text = re.sub("PRESENTMVP",
                          "PRESENT MVP",
                          new_text)
        new_text = re.sub("regarding data related projectsDATA ANALYTICS",
                          "regarding data related projects DATA ANALYTICS",
                          new_text)
        new_text = re.sub("2021ATLANTBH",
                          "2021 ATLANTBH",
                          new_text)
        new_text = re.sub("high proﬁle clientsDATA ENGINEERING",
                          "high proﬁle clients DATA ENGINEERING",
                          new_text)
        new_text = re.sub("2020SYMPHONY",
                          "2020 SYMPHONY",
                          new_text)
        new_text = re.sub("ML-driven pipelinesDATA ANALYTICS",
                          "ML-driven pipelines DATA ANALYTICS",
                          new_text)
        new_text = re.sub("2018ATLANTBH",
                          "2018 ATLANTBH",
                          new_text)
        new_text = re.sub("EMPLOYMENT RECORD10/2021 - PresentData EngineerMVP Match03/2020 - 10/2021Lead Data AnalystAtlantbh06/2018 - 03/2020Data EngineerSymphony10/2015 - 06/2018Data AnalystAtlantbh10/2015 - 02/2017Teaching assistantSarajevo School of Science and Technology05/2015 - 08/2015Software development internshipAuthority Partners",
                          " EMPLOYMENT RECORD 10/2021 - Present Data Engineer MVP Match 03/2020 - 10/2021 Lead Data Analyst Atlantbh 06/2018 - 03/2020 Data Engineer Symphony 10/2015 - 06/2018 Data Analyst Atlantbh 10/2015 - 02/2017 Teaching assistant Sarajevo School of Science and Technology 05/2015 - 08/2015 Software development internship Authority Partners",
                          new_text)
        return new_text
    
    
    def extract_features(self, text):
        """Extracts basic features from the text

        Parameters
        ----------
        text : str
            The text on which the re module will be applied

        Returns
        ------
        Dict containing basic features
        """
        # Name
        name = re.search(r"\w+\s\w+", text).group()
        # Role
        role = re.search(r"\w+\s\w+\s/\s\w+\s\w+", text).group()
        # Geolocation
        geo = re.search(r"\w+,\s[A-Z][a-z]+\s\w+\s[A-Z][a-z]+", text).group()
        # Email
        email = re.search(r"[\w]+@[\w.]+", text).group()
        # Phone
        phone = re.search(r"\+\d{3}\s\d{2}\s\d{3}\s\d{3}", text).group()
        # Data keywords
        data_bigrams = re.findall(r"DATA\s\w+", text)
        # Declared experience
        experience = re.search(r"\d+\syears", text).group()
        # Education
        education = re.search(r"[A-Z][a-z]+\s\w+,\s[\w\s]+,\s[\w\s]+–[\w\s]+", text).group()
        # Thesis
        thesis = re.search(r"[\w\s]+:[\w\s]+", text).group()
        # Projects
        # projects = [x.group() for x in re.finditer(r"\w+\s\w+\s\|\s[\w\s]+\|[\w\s\d]+[–-]\s(PRESENT|\w+\s\d+)", text)]
        projects = [x.group() for x in re.finditer(r"(SYMPHONY\s\|[\w\s()]+\|[\w\s\d(),+ﬂ]+)|(\w+\s\w+\s\|\s[\w\s]+\|[\w\s\d]+[–-]\s(PRESENT|\w+\s\d+))", text)]
        # Tasks
        tasks = re.findall(r"·\s[\w\s,()'/-]+", text)
        # Employee record
        emp_rec = [x.group() for x in re.finditer(r"\d{2}/\d{4}\s-\s(\d{2}/\d{4}|Present)\s[\D\s]+", text)]
        
        feature_dict = {
            'name': name,
            'role': role,
            'geolocation': geo,
            'email': email,
            'phone': phone,
            'data_bigrams': data_bigrams,
            'experience': experience,
            'education': education,
            'thesis': thesis,
            'projects': projects,
            'tasks': tasks,
            'emp_record': emp_rec
            }
        # print(feature_dict)
        return feature_dict
        
        
        
    def normalize_text(self, text):
        """Normalizes text by removing punctuations, digits, spaces, etc.

        Parameters
        ----------
        text : str
            The text on which the normalization will be applied

        Returns
        ------
        Normalized text in a string format
        """
        # Case convert - lower case
        lower_string = text.lower()
        # Remove numbers
        no_number_string = re.sub(r'\d+', '', lower_string)
        # Remove punctuations
        no_punc_string = re.sub(r'[^\w\s]', ' ', no_number_string)
        # Remove white space
        no_wspace_string = no_punc_string.strip()
        # Convert string to list of words
        lst_string = [no_wspace_string][0].split()
        # Remove stopwords
        no_stpwords_string=""
        for i in lst_string:
            if not i in stop_words:
                no_stpwords_string += i + ' '
        return no_stpwords_string
    
    
    def k_most_freq_words(self, text, freq_count):
        """Searches for k most common words appearing in the document

        Parameters
        ----------
        text : str
            The text on which the search will be applied
        freq_count : int
            The k - how much common words we want to return

        Returns
        ------
        Counter object containing k most common words
        """
        split_it = text.split()
        # Pass the split_it list to instance of Counter class.
        counter = Counter(split_it)
        # Most_common() produces k frequently encountered
        most_occur = counter.most_common(freq_count)
        # print(most_occur)
        return most_occur
    
    
    def create_wordcloud(self, text):
        """Creates and plots a text based word cloud

        Parameters
        ----------
        text : str
            The text on which the wordcloud will be based on
        """
        stopwords = set(STOPWORDS)
        
        wordcloud = WordCloud(width = 800, height = 800,
            background_color ='white',
            stopwords = stopwords,
            min_font_size = 10).generate(text)
        
        # Plot the WordCloud image                      
        plt.figure(figsize = (8, 8), facecolor = None)
        plt.imshow(wordcloud)
        plt.axis("off")
        plt.tight_layout(pad = 0)
        plt.show()
        
        
    def extract_image(self):
        """Searches for images in the document and saves them in the same directory
        """
        # Open the file
        pdf_file = fitz.open(self.path)
          
        # Iterate over PDF pages
        for page_index in range(len(pdf_file)):
            # Get the page itself
            page = pdf_file[page_index]
            image_list = page.get_images()
              
            # Printing number of images found in this page
            if image_list:
                print(f"[+] Found a total of {len(image_list)} images in page {page_index}")
            else:
                print("[!] No images found on page", page_index)
            for image_index, img in enumerate(page.get_images(), start=1):
                # Get the XREF of the image
                xref = img[0]
                # Extract the image bytes
                base_image = pdf_file.extract_image(xref)
                image_bytes = base_image["image"]
                # Get the image extension
                image_ext = base_image["ext"]
                # Load it to PIL
                image = Image.open(io.BytesIO(image_bytes))
                # Save it to local disk
                image.save(open(f"image{page_index+1}_{image_index}.{image_ext}", "wb"))
                
                
    def skill_extractor(self, skill_list, dict_key, tokens, skill_dict):
        """Helper method which extracts tech skills based on a criteria

        Parameters
        ----------
        skill_list : list
            The skills required for a key
        dict_key : str
            The key that is being evaluated
        tokens : list
            The keyword list on which the skills are being searched
        skill_dict : dict
            The final dict which will be populated with skills
            
        Returns
        ------
        List containing found values for the given key from the corpus
        """
        result = []
        counter = 0

        for skill in skill_list:
            if skill in tokens:
                result.append(skill)
                counter += 1
        return result
                     
                
    def extract_tech_features(self, normalized_text):
        """Method which collects the tech skills from the corpus

        Parameters
        ----------
        normalized_text : str
            The text on which the search will be applied

        Returns
        ------
        Dict containing the final skillset
        """
        tokens = normalized_text.split()
        
        skill_dict = {}
        
        skill_map_dict = {
            'programming': ['python', 'java', 'scala', 'c'],
            'dbs': ['mysql', 'mongo', 'cassandra', 'postgresql', 'sql', 'oracledb', 'neo4j'],
            'geospatial': ['postgis', 'arcgis', 'geoserver', 'geotiff'],
            'warehouses': ['redshift', 'snowflake', 'bigquery'],
            'processing': ['pandas', 'spark', 'pyspark', 'databricks'],
            'visualization': ['matplotlib', 'seaborn', 'tableau', 'powerbi'],
            'ml': ['classification', 'regression', 'clustering', 'ai', 'sklearn'],
            'time series': ['arima', 'sarima', 'prophet', 'lstm'],
            'scraping': ['scrappy', 'bs4', 'scrapping'],
            'backend': ['django', 'flask', 'fastapi'],
            'frontend': ['html', 'css', 'js', 'bs', 'bootstrap'],
            'version control': ['git', 'svn', 'mercurial'],
            'orchestration': ['airﬂow', 'luigi', 'nifi'],
            'containerization': ['docker', 'k8s', 'kubernetes'],
            'cloud': ['aws', 'azure', 'gcp'],
            'degree': ['bachelors', 'masters', 'phds']
            }
        
        for key, value in skill_map_dict.items():
            skillset = self.skill_extractor(value, key, tokens, skill_map_dict)
            skill_dict[key] = skillset
        return skill_dict
    
    
    def score(self, skill_dict):
        """Method which scores the candidate based on the tech skills

        Parameters
        ----------
        skill_dict : normalized_text
            The text on which the search will be applied

        Returns
        ------
        Float showing the candidate score related to the role
        Int containing an overall score which is just a sum of all skills
        """
        counter = 0
        data_analyst_skillset = ['programming', 'dbs', 'geospatial', 'visualization', 'degree', 'cloud']
        for skill in data_analyst_skillset:
            if skill_dict[skill] != []:
                counter += 1
        candidate_score = round(counter/len(data_analyst_skillset), 2)
        overall_score = sum([actual_skill != [] for actual_skill in list(skill_dict.values())])
        print(f'Candidate score: {counter}/{len(data_analyst_skillset)} ({candidate_score * 100}%)')
        return candidate_score, overall_score
            

if __name__ == "__main__":
    cv = PDFCV("MockWithPicture Anis Borcak CV Dec2021.pdf")
    meta = cv.get_pdf_metadata()
    text = cv.pdf_to_text()
    clean_text = cv.clean_text(text)
    basic_features = cv.extract_features(clean_text)
    normalized_text = cv.normalize_text(clean_text)
    cv.create_wordcloud(normalized_text)
    most_common = cv.k_most_freq_words(normalized_text, 10)
    cv.extract_image()
    tech_features = cv.extract_tech_features(normalized_text)
    candidate_score, overall_score = cv.score(tech_features)