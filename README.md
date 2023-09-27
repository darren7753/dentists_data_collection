# Scraping Dentists' Information

This project was commissioned by a client. If you're interested in similar work, check out my freelance data analyst profile on [Fastwork](https://fastwork.id/user/darren7753).

## Objective
The goal of this project was to scrape dentists' information across Indonesia, specifically focusing on their name, address, and phone number. The data was sourced from the following links:
- [Pelayanan Kesehatan - Praktek Mandiri](https://yankes.kemkes.go.id/praktekmandiri/cari/index/?propinsi=&kabkota=&kategori=5&nama=Gigi)
- [Pelayanan Kesehatan - Klinik (Gigi)](https://yankes.kemkes.go.id/klinik/cari?propinsi=&kabkota=&jenis=&nama=gigi)
- [Pelayanan Kesehatan - Klinik (Dental)](https://yankes.kemkes.go.id/klinik/cari?propinsi=&kabkota=&jenis=&nama=dental)
- [Pelayanan Kesehatan - Rumah Sakit (Gigi)](https://yankes.kemkes.go.id/rumahsakit/cari?propinsi=&kabkota=&namapelayanan=&namarumahsakit=gigi)
- [Ikatan Ortodontis Indonesia](https://www.ikorti-iao.com/direktori)

## Implementation
To carry out the scraping process, I utilized Selenium. Since each link presents its own unique format, especially the fifth link which is vastly different from the others, I crafted a dedicated script for each source. For instance, `scraping_1_link.py` corresponds to the first link, automated by `scraping_1_link.yml` for GitHub Actions and the data is saved in the `Data` folder. This pattern was followed for the remaining links. Post-scraping, all data collected from the individual sources was unified into a single Excel file, ensuring a comprehensive dataset.

Thank you for reviewing this repository. Please don't hesitate to reach out for further information or collaboration opportunities.
