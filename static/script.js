function fetchDataAndCreateElements(url, targetElementId, textProperty) {
  fetch(url)
    .then((response) => response.json())
    .then((response) => {
      const recordset = response;
      const targetElement = document.getElementById(targetElementId);
      for (let j = 0; j < recordset.length; j++) {
        const record = recordset[j];
        const optionElement = document.createElement("option");
        optionElement.innerText = record[textProperty];
        optionElement.value = record[textProperty];
        targetElement.appendChild(optionElement);
      }
    });
}

function addElement(tag, textToAdd, whereToAdd) {
  const addedElement = document.createElement(tag);
  addedElement.innerText = textToAdd;
  whereToAdd.appendChild(addedElement);
}

const urlForEvidence = `/evidence.json?`;
fetchDataAndCreateElements(urlForEvidence, "dowod", "item");

const urlForCrime = `/crime.json?`;
fetchDataAndCreateElements(urlForCrime, "przestepstwo", "CrimeType");

const urlParams = new URLSearchParams(window.location.search);
const firstName = urlParams.get("imie");
const lastName = urlParams.get("nazwisko");
const age = urlParams.get("wiek");
const crime = urlParams.get("przestepstwo");
const evidence = urlParams.get("dowod");

// Create search query string
const params = {
  firstName: firstName,
  lastName: lastName,
  age: age,
  crime: crime,
  evidence: evidence,
};
document.getElementById("imie").value = firstName;
document.getElementById("nazwisko").value = lastName;
document.getElementById("wiek").value = age;
document.getElementById("przestepstwo").value = crime;
document.getElementById("dowod").value = evidence;
const queryString = new URLSearchParams(params).toString();
const url = `/Criminal.json?${queryString}`;

// Fetch data from server and create HTML elements
fetch(url)
  .then((response) => response.json())
  .then((response) => {
    const grid = document.getElementById("grid");
    const grupedById = _.groupBy(response, "id");
    for (let crimeKey in grupedById) {
      const grupedByCrimeId = _.groupBy(grupedById[crimeKey], "CrimeId");
      const criminal = grupedById[crimeKey][0];

      addElement("h3", criminal.FirstName, grid);
      addElement("h3", criminal.LastName, grid);
      addElement("h3", criminal.Gender == "Male"?"Meszczyzna":"Kobieta", grid);
      addElement("h3", criminal.age, grid);
      addElement("span", criminal.Appearence, grid);

      const crimeList = document.createElement("ul");
      grid.appendChild(crimeList);
      for (let crimeKey in grupedByCrimeId) {
        addElement("li", grupedByCrimeId[crimeKey][0].CrimeDescription+" w "+ grupedByCrimeId[crimeKey][0].PlaceOfCrime, crimeList);

        const evidenceList = document.createElement("ul");
        crimeList.appendChild(evidenceList);

        for (let evidenceKey in grupedByCrimeId[crimeKey]) {
          addElement("li", grupedByCrimeId[crimeKey][evidenceKey].EvidenceItem, evidenceList);
        }
      }
      addElement("h3", criminal.victimName +" "+ criminal.victimLastName, grid);
    }
  });

const modal = document.getElementById("login");

window.onclick = function (event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
};
