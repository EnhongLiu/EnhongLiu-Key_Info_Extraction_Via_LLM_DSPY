train_example_list = [
    """
    {
        "position_title": "Derrickhand",
        "location": "Buckhannon, West Virginia 26201",
        "work_arrangement": "On-Site, Shifts",
        "experience": "1-2 years of Derrickhand experience",
        "employment_type": "Full-time",
        "pay": "Not specified",
        "degree": "High school diploma/GED or equivalent",
        "certification": "CDL B License",
        "required_skills": "Effective verbal/written communication in English, ability to interact with teams in a fast-paced environment, ability to multi-task, basic problem solving, organizational skills, excellent customer-service"
    }
    """,
    """
    {
        "position_title": "Pharmacy Technician",
        "location": "San Quentin, California",
        "work_arrangement": "On-Site, Shifts, Relocation required if applicable",
        "experience": "1 year of experience as Pharmacy Technician",
        "employment_type": "Contract",
        "pay": "$18-$19/hr",
        "degree": "High school diploma or GED",
        "certification": "Pharmacy Technician Certification, BLS Certification",
        "required_skills": "Excellent communication skills, ability to use computer for day-to-day tasks, basic math for counting medications"
    }
    """,
    """
    {
        "position_title": "GIS Technician",
        "location": "Oklahoma City, OK 73134",
        "work_arrangement": "On-Site, Shifts, Relocation required if applicable",
        "experience": "3-5 years of GIS experience",
        "employment_type": "Full-time",
        "pay": "Not specified",
        "degree": "Bachelor's degree in a related field",
        "certification": "Not specified",
        "required_skills": "GIS, ArcPy, ESRI ArcGIS Desktop or ArcPro, Field Maps/ArcGIS Online, Microsoft Office suites, clerical skills, ability to work in a team environment, initiative in recognizing need for improvements of existing systems, tracking down msising/misfiled items, filing accuracy"
    }
    """,
    """
    {
        "position_title": "Graphic Designer",
        "location": "Goochland, VA",
        "work_arrangement": "Hybrid, with two in-office days per week",
        "experience": "Minimum 5 years design and publications experience",
        "employment_type": "Part-time",
        "pay": "Not specified",
        "degree": "College degree in graphic design, visual arts, or related field",
        "certification": "Not specified",
        "required_skills": "proficiency with InDesign, Photoshop, Illustrator, working knowledge of Constant Contact, strong organizational skills, excellent oral/written communication and client-relations skills, ability to work under pressure, working knowledge of AP style, 35mm and digital photography skills, Mac environment"
    }
    """,
    """
    {
        "position_title": "Senior Cybersecurity Analyst",
        "location": "Washington DC, USA",
        "work_arrangement": "Not Specified",
        "experience": "5 years of experience in cybersecurity",
        "employment_type": "Full-time",
        "pay": "Not specified",
        "degree": "Bachelor's degree",
        "certification": "DOD 8570 Level II, DOD 8570 Level III or Manager",
        "required_skills": "carbon black implementation, splunk, CDM dashboards, CI/CD, black box testing of IT assets"
    }
    """,
    """
    {
        "position_title": "Academic Instructor",
        "location": "Fullerton, CA",
        "work_arrangement": "Not specified",
        "experience": "Experience working with low-income and diverse student population, experience working with AUHSD student, experience working with middle or high school students",
        "employment_type": "Part-time",
        "pay": "$47-$52/hr",
        "degree": "Bachelor's degree, Master's degree",
        "certification": "Not specified",
        "required_skills": "Teaching, ability to work in a collaborative team environment, develop effective teaching strategies, lifting of up to 25lbs"
    }
    """,
    """
    {
        "position_title": "Retail Scan Associate",
        "location": "Luverne, Minnesota",
        "work_arrangement": "On-site",
        "experience": "Not specified",
        "employment_type": "Part-time",
        "pay": "$16/hr",
        "degree": "High school diploma/GED",
        "certification": "Not specified",
        "required_skills": "Ability to endure being on your feet for long periods of time, ability to lift up to 25lbs, reach 6 feet in the air, ability to perform repetitive movements with hands, wrists, arms, and legs, attention to detail and ability to work independently"
    }
    """,
    """
    {
        "position_title": "Machinist Operator",
        "location": "Valencia, CA",
        "work_arrangement": "On-site, Shifts",
        "experience": "3 years of CNC operating and programming experience, experience with BobCad",
        "employment_type": "Full-time, Temp-to-Hire",
        "pay": "$30/hr",
        "degree": "High school diploma/GED",
        "certification": "BobCad, Solid Works, HAAS ST 20, Fadal WMC4020, Akira-Seiki SL20",
        "required_skills": "Strong math, problem solving and analytical skills"
    }
    """,
    """
    {
        "position_title": "Automotive Technician",
        "location": "Bremerton, WA",
        "work_arrangement": "On-site",
        "experience": "4-7 years of experience",
        "employment_type": "Full-time",
        "pay": "$50,000 - $83,200 a year",
        "degree": "High school diploma",
        "certification": "Not specified",
        "required_skills": "capable of diagnosing and repairing any system of the automobile to dealership and manufacturer's standards without supervision"
    }
    """,
    """
    {
        "position_title": "Industrial Maintenance Electrician",
        "location": "Cary, NC",
        "work_arrangement": "On-site, Shifts",
        "experience": "previous experience working in a food manufacturing plant",
        "employment_type": "Full-time",
        "pay": "$30.53/hr",
        "degree": "High school diploma/GED",
        "certification": "Not specified",
        "required_skills": "Basic computer skills including Microsoft Office, Demonstrated knowledge of behavior-based safety systems, ability to lift up to 50lbs"
    }
    """,
    """
    {
        "position_title": "Technician",
        "location": "Palm Harbor, FL",
        "work_arrangement": "On-site",
        "experience": "5+ years of service technician experience, 10+ preferred",
        "employment_type": "Full-time",
        "pay": "$27K - $66K",
        "degree": "High school diploma/GED",
        "certification": "ASE Certification, Diagnostic, Electric and Engine Repair",
        "required_skills": "excellent hand-eye coordination, mechanical and troubleshooting skills, ability to operate electronic diagnostic equipment, excellent customer service skills, basic computer competencies, ability to collaborate with others, ability to learn new technology"
    }
    """,
    """
    {
        "position_title": "Director of Email Marketing",
        "location": "Austin, TX",
        "work_arrangement": "Not specified",
        "experience": "5+ years of experience as project manager",
        "employment_type": "Full-time",
        "pay": "$125,000 - $250,000 a year",
        "degree": "Bachelor's degree in marketing",
        "certification": "Not specified",
        "required_skills": "Ability to collaborate with a team of people to learn and grow and own new responsibilities, sophisticated verbal and written communication, people, and leadership skills, advanced analytical and problem-solving skills, focus on email marketing, experience with testing and activating cold audiences, experience with project methodologies including agile, waterfall, and scrum, experience having worked at a startup or a small company with less than 50 people"
    }
    """,
    """
    {
        "position_title": "Campus Store Leader",
        "location": "Philadelphia, PA",
        "work_arrangement": "On-site",
        "experience": "0-5 years of relevant experience, retail experience is a plus",
        "employment_type": "Full-time",
        "pay": "$15.00 - $21.56 an hour",
        "degree": "Associate's degree",
        "certification": "Not specified",
        "required_skills": "analysis skills, computer skills, financial acumen, communication skills, time management, advanced relationship building, ability to influence a team, customer outreach"
    }
    """,
    """
    {
        "position_title": "Dental Laboratory Technician",
        "location": "Wood Dale, IL",
        "work_arrangement": "On-site",
        "experience": "5 years of Fabrication experience",
        "employment_type": "Part-time, Contract",
        "pay": "$14.00 - $22.00 per hour",
        "degree": "High school diploma or equivalent",
        "certification": "Not specified",
        "required_skills": "3Shape software savvyy, Fabrication of custom trays, bite rims, denture/partial repairs"
    }
    """,
   

 """
    {
        "position_title": "Senior Data Engineer (Machine Learning)",
        "location": "Wood Dale, IL",
        "work_arrangement": "Remote",
        "experience": "5+ years of experience as a Data Engineer",
        "employment_type": "Full-time, Direct Hire",
        "pay": "$130,000 - $170,000 per year",
        "degree": "Bachelor's degree in computer science, engineering, or data science",
        "certification": "Not specified",
        "required_skills": "focused on Python, Postgres, and DBT, Experience using Google Cloud Platform and ideally Google AI tools, Experience with data modeling, data warehousing, and building ETL pipelines with DBT, Python, Postgres, DBT, SQL, PostgreML, TensorFlow, PyTorch, Google BigQuery, Airflow, Fivetran, Make, excellent understanding of machine learning algorithms, processes, tools and platforms, proven ability to drive business results with data-based insights"
    }
    """,
    """
    {
        "position_title": "Solutions Architect",
        "location": "Mayfield Heights, OH",
        "work_arrangement": "Not Specified",
        "experience": "Minimum 2 years of experience",
        "employment_type": "Full-time",
        "pay": "$64.7K - $81.9K a year",
        "degree": "Bachelors Degree in Information Technology, MIS, or Financial Accounting, Advanced diploma/degree in Finance/Management Accounting preferred",
        "certification": "CPA Certification preferred, Certification in SAP FICO highly preferred",
        "required_skills": "supporting SAP FI/CO modules and related integration with MM and SD SAP AP, AR, COPA and COPC, Minimum of 2 full SAP life-cycle implementations, and upgrades, Experience with SAP S/4 HANA Upgrade a plus, SAP FI/CO modules, MM, SD, SAP, AP, AR, COPA, COPC"
    }
    """,
    """
    {
        "position_title": "Marketing Manager",
        "location": "Andover, NJ 07821",
        "work_arrangement": "Remote",
        "experience": "Minimum of 2 years in marketing & social media management preferred, demonstrable experience with social analytics tools",
        "employment_type": "Full-time, Shift and schedule weekends as needed, nights as needed",
        "pay": "$60,000 a year",
        "degree": "Bachelor's degree in marketing, communications, or related field",
        "certification": "Not specified",
        "required_skills": "excellent writing, editing(photo/video/text), presentation, and communication skills, ability to work nights and weekends as needed"
    }
    """,
    """
    {
        "position_title": "Technical Project Manager",
        "location": "Santa Monica, CA",
        "work_arrangement": "On-site",
        "experience": "4-7 years of experience in project management",
        "employment_type": "Full-time",
        "pay": "$78,000 - $150,000",
        "degree": "Bachelor's degree in a hardware or software engineering field",
        "certification": "PMP or similar certification",
        "required_skills": "Ability to effectively communicate project milestones, status, and risks at all levels of the organization, delivering consumer, enterprise, or industrial products, experience managing all steps of the product lifecycle from concept to manufacturing, experience simultaneously managing different projects with multiple stakeholders, demonstrated experience developing or deploying applications of interactive, AR, VR, or XR, experience as a scrum master or similar agile processes, experience interfacing with test teams, experience working on defense & aerospace products"
    }
    """,
    """
    {
        "position_title": "Logistics Coordinator",
        "location": "Henderson, NV 89074",
        "work_arrangement": "On-site",
        "experience": "previous experience in operations or a related field is a plus",
        "employment_type": "Full-time, Shift",
        "pay": "From $14 an hour",
        "degree": "High school diploma/GED",
        "certification": "Not specified",
        "required_skills": "Excellent organizational and inter-personal and communication skills, strong organizational and multitasking abilities, proficiency in Microsoft Office and other relevant software"
    }
    """,
    """
    {
        "position_title": "Sr. Net Developer with AWS",
        "location": "Irving, TX",
        "work_arrangement": "On-site",
        "experience": "Experience with microservices, cloud services, especially with AWS, 2+ years of experience",
        "employment_type": "Full-time, Contract 12+ Months",
        "pay": "Not specified",
        "degree": "Bachelor's/Master's in computer science or related fields",
        "certification": "AWS certified(associate or professional)",
        "required_skills": "proficiency with C#, .NET Core framework 2.x & higher, Git, SVN, MongoDB, Cassandra, familiarity with dev-ops software development methods and Docker container related technologies"
    }
    """
]