const halfWidth = window.innerWidth / 2;
const halfHeight = window.innerHeight / 2;

const connection = new WebSocket("ws://localhost:9999/");
connection.onopen = (e) => {
  console.log("onopen");
};

const div = document.getElementById("canvas");

const saiaku = (d, text) => {
  const data = d;
  const textContent = text;
  console.log(textContent);
  const list = [
    `<div class="transitions" style="width: 600px; 
  position:absolute; top: ${data.t}px; right:${data.r}px;);">
  <p class="text" style="font-size: 5vh";>${data.scene_num}</p> 
  ${textContent}
  </div>`,
    `<div class="transitions" style="width: 600px; 
  position:absolute; top: ${data.t}px; left:${data.l}px;);">
  <p class="text" style="font-size: 20px";>${data.scene_num}</p> 
  ${textContent} 
  </div>`,
    `<div class="transitions" style="width: 600px; 
  position:absolute; bottom: ${data.b}px; right:${data.r}px;);">
  <p class="text" style="font-size: 20px";>${data.scene_num}</p> 
  ${textContent} 
  </div>`,
    `<div class="transitions" style="width: 600px; 
  position:absolute; bottom: ${data.b}px; left:${data.l}px;);">
  <p class="text" style="font-size: 20px";>${data.scene_num}</p> 
  ${textContent} 
  </div>`,
  ];
  console.log(list[data.f]);
  return list[data.f];
};

connection.onmessage = (e) => {
  let text = "";
  const data = JSON.parse(e.data);
  //document.getElementById("sample").textContent = JSON.parse(e.data)["texts"];
  console.log(e.data);
  data.texts.forEach((name) => {
    text += `<p id="sample" class="text">
      <span>${name}<span/>
      </p>`;
  });
  console.log(text);
  const test = saiaku(data, text);
  console.log(test);
  div.insertAdjacentHTML("afterbegin", test);
  fitty("#sample");
};

document.addEventListener(
  "webkitAnimationStart",
  (event) => {
    if (event.animationName == "fadeout") {
      const dom = event.target;
      dom.style.transformOrigin = `(${innerWidth}, ${innerHeight})`;
      const left = dom.offsetLeft;
      const top = dom.offsetTop;
      const width = dom.offsetWidth;
      const height = dom.offsetHeight;
      const center = left + width / 2;
      const center2 = top + height / 2;

      const moveX = halfWidth - center;
      const moveY = halfHeight - center2;
      console.log(dom.textContent + "X:" + moveX + ",Y:" + moveY);
      console.log(halfWidth, halfHeight);
      console.log(center, center2);
      dom.style.transition = " cubic-bezier(0.75, 0.21, 0.83, 0.67) 4s";
      dom.style.transitionDelay = "0.1s";
      dom.style.transformOrigin = `(${center}px, ${center2}px)`;
      dom.style.transform = `translate(${moveX}px, ${moveY}px) scale(0.2)`;
    }
  },
  true
);
