const fs = require("fs");
const csv = require("csv-parser");

const data = [];

fs.createReadStream("./data/vat_dung_an_uong(2).csv") // Đường dẫn đến file CSV
  .pipe(csv()) // Sử dụng csv-parser để phân tích
  .on("data", (row) => {
    if (row.file_url.trim() !== "") {
      row.file_url = row.file_url.slice(0, -2);
    }
    let images = row.file_url.split("--");

    if (row.product_option !== "No option") {
      row.product_option = row.product_option.slice(0, -2).split("--");
    }
    row.file_url = images;
    row.name = row.name;
    data.push(row);
  })
  .on("end", () => {
    console.log(data);
    try {
      const jsonData = JSON.stringify(data, null, 2);
      fs.writeFileSync("vat_dung_an_uong.json", jsonData); // Ghi tệp
      console.log("Tệp JSON đã được ghi thành công!");
    } catch (err) {
      console.error("Lỗi khi ghi tệp:", err);
    }
  });
