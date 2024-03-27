"use strict";
 
$(document).ready(function () {
  const url =
    "https://raw.githubusercontent.com/ashhadulislam/JSON-Airports-India/master/airports.json";
  // "http://127.0.0.1:8000/post/postAPI/?format=json";
  fetch(url)
    .then((response) => {
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      return response.json();
    })
    .then((data) => {
      const citiesWithCodes = data.airports.map((airport) => ({
        cityName: airport.city_name,
        IATACode: airport.IATA_code,
      }));
 
      populateCitiesList(citiesWithCodes, "cityInputFrom", "citiesListFrom");
      populateCitiesList(citiesWithCodes, "cityInputTo", "citiesListTo");
    })
    .catch((error) => {
      console.error("There was a problem fetching the data:", error);
    });
 
  function populateCitiesList(citiesWithCodes, inputId, dataListId) {
    const datalist = document.createElement("datalist");
    datalist.id = dataListId;
 
    citiesWithCodes.forEach((city) => {
      const option = document.createElement("option");
      option.value = `${city.cityName} (${city.IATACode})`;
      datalist.appendChild(option);
    });
 
    const existingDatalist = document.getElementById(dataListId);
    if (existingDatalist) {
      existingDatalist.parentNode.removeChild(existingDatalist);
    }
 
    document.body.appendChild(datalist);
 
    const cityInput = document.getElementById(inputId);
    cityInput.setAttribute("list", dataListId);
 
    cityInput.addEventListener("input", function () {
      const inputText = this.value.toLowerCase();
      const matchingCities = citiesWithCodes.filter(
        (city) =>
          city.cityName.toLowerCase().includes(inputText) ||
          city.IATACode.toLowerCase().includes(inputText)
      );
 
      showCities(matchingCities, dataListId);
    });
 
    function showCities(matchingCities, dataListId) {
      const datalist = document.createElement("datalist");
      datalist.id = dataListId;
 
      matchingCities.forEach((city) => {
        const option = document.createElement("option");
        option.value = `${city.cityName} (${city.IATACode})`;
        datalist.appendChild(option);
      });
 
      const existingDatalist = document.getElementById(dataListId);
      if (existingDatalist) {
        existingDatalist.parentNode.removeChild(existingDatalist);
      }
 
      document.body.appendChild(datalist);
      cityInput.setAttribute("list", dataListId);
    }
  }
});
 
function menuToggle() {
  const toggleMenu = document.querySelector(".menu");
  toggleMenu.classList.toggle("active");
}
 
document.addEventListener("click", function (event) {
  const menu = document.querySelector(".menu");
  const profile = document.querySelector(".profile");
 
  // Check if the clicked element is not within the menu or profile
  if (!menu.contains(event.target) && !profile.contains(event.target)) {
    menu.classList.remove("active");
  }
});
 
const container = document.createElement("div");
container.classList.add("container");
 
const row = document.createElement("div");
row.classList.add("row", "row-cols-1", "row-cols-sm-2", "row-cols-md-3", "g-3");
 
const albumDiv = document.createElement("div");
albumDiv.classList.add("album", "py-5", "bg-body-tertiary");
 
// Create albumDiv if it doesn't exist
if (!albumDiv) {
  albumDiv = document.createElement("div");
  albumDiv.id = "albumDiv";
  document.body.appendChild(albumDiv);
}
async function fetchData(flightNumber, source, destination, dateOfJourney) {
  try {
    const response = await fetch(
      `http://98.70.12.179:8000/app1/postAPI/?flight_number=${flightNumber}&source=${source}&destination=${destination}&date_of_journey=${dateOfJourney}`
    );
 
    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }
    const data = await response.json();
    return data;
  } catch (error) {
    console.error("Error fetching data:", error);
    return [];
  }
}
 
document.addEventListener("DOMContentLoaded", () => {
  fetchData("", "", "", "")
    .then((result) => {
      res = result;
      console.log(res);
      createCardStructure(res);
    })
    .catch((error) => {
      console.error("Error:", error);
    });
});
async function createCardStructure(filteredData) {
  try {
    const container = document.createElement("div");
    container.classList.add("container");
 
    const row = document.createElement("div");
    row.classList.add(
      "row",
      "row-cols-1",
      "row-cols-sm-2",
      "row-cols-md-3",
      "g-3"
    );
    if (!filteredData || filteredData.length === 0) {
      // document.body.innerHTML = "";
      var noPostsMessage = document.createElement("div");
      noPostsMessage.classList.add("no-posts-message");
      var messageContent = document.createElement("div");
      messageContent.innerHTML =
        "<h1>No posts found <i class='far fa-frown' width=30px, height=30px></i></h1> ";
      // Create a new HTML element for the message
      noPostsMessage.appendChild(messageContent);
      // Append the message to the body
      row.appendChild(noPostsMessage);
    }
 
    // const currentUserID = "{{ user.id }}";
 
    // const container = document.createElement("div");
    // container.classList.add("container");
 
    // const row = document.createElement("div");
    // row.classList.add('row', 'row-cols-1', 'row-cols-sm-2', 'row-cols-md-3', 'g-3');
    filteredData.forEach((data, index) => {
      const col = document.createElement("div");
      col.classList.add("col");
 
      const card = document.createElement("div");
      card.classList.add("card", "shadow-sm");
 
      const cardBody = document.createElement("div");
      cardBody.classList.add("card-body");
 
      // console.log("data.user:", data.user);
      // console.log(data.passenger_name);
      // console.log("currentUserID:", currentUserID);
      const isCurrentUserPost = data.user == currentUserID;
      // console.log("isCurrentUserPost:", isCurrentUserPost);
 
      const content = `
                <div class="d-flex justify-content-around">
                  <span class="iata-code">${data.source.split(" ").pop()}</span>
                  <img src="/static/Post/images/flight.png" alt="Flight Symbol" class="flight-symbol" />
                  <span class="iata-code">${data.destination
                    .split(" ")
                    .pop()}</span>
                </div>
              <div class="dept">
                  <p>${data.source}</p>
                  <p>${data.date_of_journey}</p>
                  <p>${data.destination}</p>
              </div>
              <div class="first">
                  <p>${data.flight_number}</p>
                  <p>${data.passenger_name}</p>
              </div>
              <div class="second">
                  <p>${data.pnr_number}</p>
                  <button type="button" class="btn btn-success verify" id="verification_${index}"  onclick="redirectToWingie('${data.pnr_number}')">Verify PNR</button>
              </div>
              <div class="third">
                  <p><b>Available Space: ${data.baggage_space}kgs</b></p>
              </div>
              <div class="fourth">
              ${
                isCurrentUserPost
                  ? `<button type="button" class="btn btn-success custom-color"  id="chat_${index}" disabled>Chat</button>`
                  : `<button type="button" class="btn btn-success custom-color" id="chat_${index}" >Chat</button>`
              }
              </div>
         
        </div>
       
          `;
 
      cardBody.innerHTML = content;
      card.appendChild(cardBody);
      col.appendChild(card);
      row.appendChild(col);
 
      if (!isCurrentUserPost) {
        const chatButton = cardBody.querySelector(`#chat_${index}`);
        chatButton.addEventListener("click", function () {
          // Assuming chat.html is in the same directory, you can change the path accordingly
          window.location.href = `/app1/chats/?roomnumber=${data.baggage_number}`;
        });
      }
    });
 
    container.appendChild(row);
    albumDiv.innerHTML = "";
    albumDiv.appendChild(container);
    document.body.appendChild(albumDiv);
  } catch (error) {
    console.error("Error creating card structure:", error);
  }
 
}
function redirectToWingie(pnrNumber) {
  // Construct the URL with the PNR number
  const wingieURL = `https://www.wingie.com/pnr-query/?pnr=${encodeURIComponent(pnrNumber)}`;
 
  // Redirect to the Wingie URL
  window.location.href = wingieURL;
}