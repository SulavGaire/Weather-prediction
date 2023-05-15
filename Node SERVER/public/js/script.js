/************************ declering variables*********************************/

const xlabels = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0];
const TC = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0];
const TF = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0];
const h = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0];
const BMPT = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0];
const BMPP = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0];
const BMPA = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0];

/************************* CHART FOR TEMPERATURE ******************************/

const ctx1 = document.getElementById("chart-1").getContext("2d");
const myChart1 = new Chart(ctx1, {
  type: "line",
  data: {
    labels: xlabels,
    datasets: [
      {
        label: "TEMPERATURE celsius",
        data: TC,
        backgroundColor: ["rgba(255, 99, 132, 0.2)"],
        borderColor: ["rgba(255, 99, 132, 1)"],
        borderWidth: 1,
      },
    ],
  },
  options: {
    layout: {
      padding: 20,
    },
  },
});

/************************* CHART FOR TEMPERATURE ******************************/

const ctx2 = document.getElementById("chart-2").getContext("2d");
const myChart2 = new Chart(ctx2, {
  type: "line",
  data: {
    labels: xlabels,
    datasets: [
      {
        label: "Temperature Fahrenheit",
        data: TF,
        backgroundColor: ["rgba(255, 99, 132, 0.2)"],
        borderColor: ["rgba(255, 99, 132, 1)"],
        borderWidth: 1,
      },
    ],
  },
  options: {
    layout: {
      padding: 20,
    },
  },
});

/************************* CHART FOR PRESSURE ******************************/

const ctx3 = document.getElementById("chart-3").getContext("2d");
const myChart3 = new Chart(ctx3, {
  type: "line",
  data: {
    labels: xlabels,
    datasets: [
      {
        label: "Humidity",
        data: h,
        backgroundColor: ["rgba(255, 99, 132, 0.2)"],
        borderColor: ["rgba(255, 99, 132, 1)"],
        borderWidth: 1,
      },
    ],
  },
  options: {
    layout: {
      padding: 20,
    },
  },
});
/************************* CHART FOR ROLL ******************************/

const ctx4 = document.getElementById("chart-4").getContext("2d");
const myChart4 = new Chart(ctx4, {
  type: "line",
  data: {
    labels: xlabels,
    datasets: [
      {
        label: "Temp BMP",
        data: BMPT,
        backgroundColor: ["rgba(255, 99, 132, 0.2)"],
        borderColor: ["rgba(255, 99, 132, 1)"],
        borderWidth: 1,
      },
    ],
  },
  options: {
    layout: {
      padding: 20,
    },
  },
});

/************************* CHART FOR PITCH ******************************/
const ctx5 = document.getElementById("chart-5").getContext("2d");
const myChart5 = new Chart(ctx5, {
  type: "line",
  data: {
    labels: xlabels,
    datasets: [
      {
        label: "Pressure",
        data: BMPP,
        backgroundColor: ["rgba(255, 99, 132, 0.2)"],
        borderColor: ["rgba(255, 99, 132, 1)"],
        borderWidth: 1,
      },
    ],
  },
  options: {
    layout: {
      padding: 20,
    },
  },
});
/************************* CHART FOR YAW ******************************/

const ctx6 = document.getElementById("chart-6").getContext("2d");
const myChart6 = new Chart(ctx6, {
  type: "line",
  data: {
    labels: xlabels,
    datasets: [
      {
        label: "Altitude",
        data: BMPA,
        backgroundColor: ["rgba(255, 99, 132, 0.2)"],
        borderColor: ["rgba(255, 99, 132, 1)"],
        borderWidth: 1,
      },
    ],
  },
  options: {
    layout: {
      padding: 20,
    },
  },
});

//builds socket connection with server to fetch dataarray and send port-number

var socket = io.connect("http://localhost:4000");

// fetch dataarray and stores in object message
socket.on("dataArray", function (message) {
  //calculate current time for x-axis
  var today = new Date();
  var time =
    today.getHours() + ":" + today.getMinutes() + ":" + today.getSeconds();
  xlabels.push(time); //push current time in xlabel(x-axis data)
  TC.push(message.dataArray[0]); //dataArray[0] contains temp data
  TF.push(message.dataArray[1]); //dataArray[1] contains ldr data
  h.push(message.dataArray[2]); //dataArray[2] contains pressure data
  BMPT.push(message.dataArray[3]); //dataArray[3] contains roll data
  BMPP.push(message.dataArray[4]); //dataArray[4] contains pitch data
  BMPA.push(message.dataArray[5]); //dataArray[5] contains yaw data

  // console.log(time);
  // console.log(message.dataArray[0]);
  // console.log(message.dataArray[1]);
  // console.log(message.dataArray[2]);
  // console.log(message.dataArray[3]);
  // console.log(message.dataArray[4]);
  // console.log(message.dataArray[5]);

  /********************* shifting the dataarray *********************/
  xlabels.shift();
  TC.shift();
  TF.shift();
  h.shift();
  BMPT.shift();
  BMPP.shift();
  BMPA.shift();

  /*********************** updating the chart ***********************/
  myChart1.update();
  myChart2.update();
  myChart3.update();
  myChart4.update();
  myChart5.update();
  myChart6.update();
});

/**************************Get the value of the input field with id="numb" (PORT-NUMBER) */
function myFunction() {
  let x = document.getElementById("numb").value;
  socket.emit("message", x); //sends portnumber to server.js
  console.log(x);
}
